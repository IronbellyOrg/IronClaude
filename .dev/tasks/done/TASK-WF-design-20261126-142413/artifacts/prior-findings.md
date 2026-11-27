# Reflect Report: pre-execution review of TASK-WF-design-20261126-131233

```yaml
contract_version: 1.9.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.73
citations_total: 58
citations_revalidated: 58
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

## Summary

**Verdict: refactor the plan before it is run.** The plan (`.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md`, 7 tasks, 158 lines) covers all seven requirements of its spec (`.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md`) in substance, and its edits, line numbers and dependents match the repository. Three findings block execution: the Task 2 mutation check cannot pass as written (M1), the plan's own format check fails on the unmodified tree in this worktree and its fix would rewrite six files the plan does not list (M2), and the plan lacks the spec's rule that the final verification is reported as blocked until there is a commit (M3). Two further Medium findings, one Note and one Tier 1 Medium do not block (see Findings). The plan was not edited; this review is advisory.

**How it was reviewed (Tier 2).** Three reviewers on different model classes (analyzer on sonnet, qa on haiku, refactorer on opus) audited the plan against the spec. Each card was re-graded blind by a separate calibrator (0.66, 0.66, 0.87). The cards were merged by an adversarial debate: two rounds with one advocate per card, an invariant probe by an independent fault-finder (10 findings, 2 HIGH), a follow-up round that settled both HIGH findings (3 of 3 advocates), scoring on two layers (base card = refactorer, 0.902 against 0.776 and 0.730), and a merge. Convergence was 95.8% (23 of 24 debate points). All 58 citations were re-read by a separate validator: 58 verified, 0 dropped.

**Tier 1 context.** The Tier 1 pass found the plan covers R-01 to R-07 in substance but names no requirement id in any task, so the mechanical coverage is 0 of 7 parsed and 21 of 31 (0.6774) with inferred rows. It escalated to Tier 2 on rubric rule 4 (three or more domains).

## Findings

### M1: Task 2 mutation check cannot pass as written

- **Grade:** Blocking (Decision)
- **Claim:** Task 2's mutation check (a plan-added acceptance check, not in source.md section 5) requires that a mutation at one site leaves "the other two site functions still pass". In Task 2, test_phase_a_depth_delegation_row is already red: Task 2's own first acceptance line says so, because line 624 yields standard and deep. So a mutation at the ref or skill site always leaves one "other" site function failing, and a mutation of the row site cannot show a new failure. Writing `--depth <d>` at the ref site (line 72) or the skill site (line 374) also fails test_no_placeholder_depth_on_sc_workflow_lines, because both lines contain sc:workflow. That breaks "only that site's function fail". A whole-text replace of `--depth standard` in `_SKILL` changes five places, both skill sites among them, so it cannot mutate one site alone (INV-001, VR-9). The check also edits refs/remediation-handoff.md, which the Constraints say not to touch. The broken-plan-check rule applies: the executor cannot satisfy this Task 2 acceptance criterion as written.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:42`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:60`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:62`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:20`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:624`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:374`; `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:72`; `tests/cli/reflect/test_remediation_route_table.py:13-16`
- **Recommendation:** In Task 2, delete the mutation-check bullet (plan:62), and require the five new test functions to take no arguments (no `parametrize`) and to read `_REF`, `_SKILL` and `_CMD` inside their bodies. In Task 7, after the line-624 edit, add this acceptance bullet: 'Mutation check, in memory only. `./artifacts/t7-mutation-check.py` in this package is run with `uv run python` from the repository root. It loads `tests/cli/reflect/test_remediation_route_table.py` from its repository path and first runs the five new tests on the unmutated text, requiring all five to pass. It then runs nine cases: for each of the ref Phase A region, the skill Phase A region and the delegation row, replace `--depth standard` with `--depth deep`, delete it, or replace it with `--depth <d>`. Each case changes only that site's own slice (the `_region` text, or the `_delegation_row()` line): it asserts the slice occurs once and holds `--depth standard` exactly once, writes the changed slice back into the module string with a single replacement, asserts the result differs from the original, calls the five tests, and restores the originals. Expected: the changed site's function fails and the other two site functions pass; the placeholder test also fails in every `<d>` case; `test_review_only_decision_stays_written_down` also fails when the row is changed to `deep`. Only AssertionError counts as a detection. The script exits nonzero on any mismatch; each case and the exit code go to `./artifacts/t7-mutation.log`. No tracked file changes. The check shows that each site's depth check can fail.'
- **Where the reviewers stood:** All three cards found the defect; the repair is the refactorer's, hardened by the invariant probe (INV-001 to INV-004, INV-010). Advocates: 3 of 3.

### M2: The plan's own format check fails on the unmodified tree

- **Grade:** Blocking (Decision)
- **Claim:** The Constraints say "fix formatting with `make format`", but that target runs `uv run ruff format .`. It formats the whole repo except docs/ and .dev/ (scripts/, plugins/ and root files included), not only the edited files. Task 1 also records no ruff baseline. If any file outside the seven planned ones is not format-clean, `make format` rewrites it. That edits outside the declared surface and makes Task 7's `git status --short` acceptance fail for an unrelated reason. A pre-existing violation in src/ or tests/ would also make Task 7's `ruff format --check src/ tests/` fail with no baseline to compare against. Observed in this worktree (VR-9): plain `uv run ruff --version` prints ruff 0.17.3, `uv run ruff check src/ tests/` exits 0, and the plan's own command `uv run ruff format --check src/ tests/` exits 1 on the unmodified tree, listing six files, none of them among the seven files Task 7's `git status --short` check allows. The pin `ruff==0.15.20` sits only in the optional `dev` extra, and the result under the pin is unverified. In this worktree no executor can satisfy Task 7's ruff check and its file list together, so correcting the text changes two acceptance checks.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:24`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:32-36`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:156`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:158`; `Makefile:53-55`; `pyproject.toml:45-54`
- **Recommendation:** In Task 1, also record `uv run ruff --version`, the exit codes of `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/`, and every file the format check lists, in `./artifacts/baseline-pytest.md`. In the Constraints, replace 'fix formatting with `make format`' with 'fix formatting with `uv run ruff format <each file you edited>`; run `make format` only if Task 1's format check exited 0, and otherwise record the departure from spec step 5 as a necessary deviation in `./artifacts/t7-checks.md`'. In Task 7, replace the ruff acceptance line (plan:156) with '`uv run ruff check src/ tests/` exits 0, and `uv run ruff format --check src/ tests/` lists no file that Task 1 did not list and none of the seven edited files; both outputs are recorded in `./artifacts/t7-checks.md`'.
- **Where the reviewers stood:** Only the refactorer card raised it (as Medium). Regraded to Blocking (Decision) after the plan's own command was run in this worktree (it exits 1 on the unmodified tree). Advocates: 3 of 3 after that result.

### M3: The spec's rule to report the final verification as blocked is missing

- **Grade:** Blocking (Missing)
- **Claim:** The spec requires that without a commit the final verification is reported as blocked. The plan names the later commit and the full-suite run but has no acceptance criterion or completion report that says so, so Task 7 can finish on the deselected reflect suite alone. No line of the plan contains the word "blocked" (VR-4); its Constraints only forbid reporting a deselected run as the complete suite.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:106`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:22`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:23`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:149-158`
- **Recommendation:** Add to the Constraints: 'Until the commit and the complete run after it, report the final verification as blocked.' In Task 7, write a named line in `./artifacts/t7-checks.md`: 'complete-suite verification: blocked until the commit'. Task 7's own result follows its acceptance criteria, not that line (a ledger task status of `blocked` is a different thing and would stop the package from being archived).
- **Where the reviewers stood:** Only the qa card raised it. Advocates: 3 of 3 on Blocking (Missing) after Round 2.

### M4: The constraint that every pytest run deselects the guard test contradicts Task 1

- **Grade:** Medium
- **Claim:** The Constraint "Every pytest run in this plan deselects exactly that node id" contradicts Task 1's bare `uv run pytest`. The bare run is correct: source.md step 1 asks for it on the unmodified tree, where the guard is green. The targeted runs in Tasks 2 to 5 also omit the flag, harmlessly, since they do not collect test_shadow_skill_contract.py; only Task 7's aggregate run carries it. `/sc:implement` treats `## Constraints` as global constraints, and a quoted breach is a blocking review trigger (`quoted-constraint-breach`), so a QA reviewer could quote this line against Task 1 (VR-8). That is a prediction, not an observed result, and no named acceptance check changes, so the grade is Medium, not Blocking.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:22`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:32`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:155`; `~/.claude/skills/sc-implement-protocol/SKILL.md:106`; `~/.claude/skills/sc-implement-protocol/refs/qa.md:52`
- **Recommendation:** In the Constraints (plan:22), replace the sentence 'Every pytest run in this plan deselects exactly that node id with ...' with: 'From the Task 7 `SKILL.md` edit until the commit, every pytest run this plan orders that collects `tests/cli/reflect/test_shadow_skill_contract.py` deselects exactly that node id. The Task 1 baseline and the complete run after the commit include it.' Keep the rest of the line.
- **Where the reviewers stood:** Raised by all three cards (analyzer and refactorer as Note, qa as Blocking). Advocates: Medium, 2 of 3; the qa advocate held Blocking (Decision).

### M5: Task 7 does not name Task 2 as a dependency

- **Grade:** Note
- **Claim:** Task 7's `Depends on` line names only Task 6, yet its acceptance check that the two tests which failed in Task 2 now pass needs the tests Task 2 adds; Task 2 has no dependents and is not an ancestor of Task 7 (VR-1). `/sc:implement` runs tasks sequentially in source order unless the source marks a set independent, and this plan marks none, so Task 2 does run first (VR-8). The missing line is a documentation defect.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:40`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:145`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:154`; `~/.claude/skills/sc-implement-protocol/SKILL.md:110`
- **Recommendation:** Change Task 7's line to 'Depends on: Task 2, Task 6'.
- **Where the reviewers stood:** Found in the debate, not by any card. Advocates: Note, 3 of 3 (`/sc:implement` runs tasks in source order).

### M6: The coverage matrix omits three spec spans

- **Grade:** Medium
- **Claim:** The coverage matrix omits requirement-bearing spans: the verdict case at source.md:92, the ordered verification procedure at source.md:100-106 and the formatting recovery and reverification at source.md:114. Its inferred rows jump from line 96 to line 113. This is an audit-evidence omission, not an extra implementation deviation. The omitted span source.md:100-106 holds the "blocked" rule of M3.
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:92`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:100-106`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:114`; `.dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/artifacts/coverage-matrix.md:37-38`
- **Recommendation:** Add inferred rows for source.md:92 (Task 3), :100-106 (Task 1 and Task 7) and :114 (Constraints and Task 7) to the coverage matrix. No change to the plan.
- **Where the reviewers stood:** Only the qa card raised it. Advocates: Medium, 2 of 3 (the analyzer advocate held Note). It concerns this review's own coverage matrix; no plan change.

### T1-F1: No task names its requirement id (Tier 1 card only)

- **Grade:** Medium (the Tier 1 grade, kept; consumer-unknown: only this review's own coverage metric reads the ids)
- **Claim:** No task in the plan names its requirement id (R-01 to R-07), so requirement-to-task traceability cannot be checked mechanically (parsed coverage 0 of 7).
- **Citations:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:17-24`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:118-126`; `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md:30-158`
- **Recommendation:** Add one line `Requirement: R-0N` under each task heading (Task 1: R-07; Task 2: R-05; Task 3: R-06; Task 4: R-03; Task 5: R-04; Task 6: R-02; Task 7: R-01 and R-07).
- **Where the reviewers stood:** Raised only by the Tier 1 card. None of the three Tier 2 reviewers raised it, and the Tier 1 calibrator called Medium generous because the spec never asks tasks to cite requirement ids. It is not part of the debate and not in the merged verdict.

Other Tier 1 card items: F2 (keep the local test helpers) is a no-change note, not a defect. F3 (the mutation check edits tracked files and relies on a manual revert) is covered by M1.

**Finding counts** (after the evidence validator): blocking 3 (M1, M2, M3), label_high 0, medium 3 (M4, M6, T1-F1), note 1 (M5).

**Notes about the input cards** (not about the plan): reviewer 1's plan citations are offset by 55 (plan:77, :87, :115, :117, :210 should read :22, :32, :60, :62, :155); reviewer 2's coverage-matrix citation (matrix:9) should read lines 37 and 38; reviewer 2 gave two grades per finding and returned a table that the orchestrator transcribed; reviewer 2's statement that spec step 1 says "without deselection" is an interpretation (`source.md:100`).

## Run notes and disclosures

- **Tiering.** Rubric rule 4 (three or more domains: code, tests, docs) fired, composite 6, so Tier 2 ran (`artifacts/tier_decision.yaml`).
- **Diversity (degraded, disclosed).** The three reviewers ran on three Anthropic model classes (one vendor). The calibrators were sonnet and opus, so the calibrator class is not disjoint from the reviewer classes (`calibrator_diversity: degraded`). The executor class could not be resolved (`executor_class_resolved: false`; the anti-self-confirmation guard is weaker). The merge orchestrator and judge was the main session (the sonnet alias), the same class as one advocate and one calibrator.
- **Cut-off replies.** Nine agent replies arrived cut off by the message size. Each time the orchestrator asked the agent to re-send only the missing part; no answer was changed. Reviewer 2 returned a table instead of the requested card; the orchestrator transcribed it field for field.
- **Checks run by the orchestrator (not reviewer findings).** Read-only commands whose results are recorded in `adversarial/adversarial/verification-results.md` (VR-1 to VR-9): the plan's Depends-on graph, grep of the spec for mutation text, ruff version and format check in this worktree (ruff 0.17.3; `uv run ruff format --check src/ tests/` exits 1 on six untouched files), the `--depth standard` count in SKILL.md, how `/sc:implement` reads Constraints and task order. The validator could not re-run the ruff commands (no shell), so the statements "ruff 0.17.3" and "six files" are grounded in those recorded runs, not in a citation. The result under the pinned ruff 0.15.20 was not tested. One of the commands (`uv run`) printed "Installed 29 packages" into the worktree's git-ignored `.venv`; the ruff version did not change and `git status` shows no tracked file changed.
- **Scoring.** The two qualitative scoring passes disagreed on 6 of 90 criterion pairs; the orchestrator re-evaluated each (`adversarial/adversarial/base-selection.md`).
- **Citation policy.** 58 citations (more than 20) would normally be sampled; all 58 were re-read, which is stricter. A pass with zero drops is suspect by rule, so the audit log carries `zero-drop-flag: true`; the orchestrator independently re-read ten of the citations while preparing the debate and they hold.
- **`confidence_calibrated` = 0.73** is the mean of the three calibrated card scores (0.66, 0.66, 0.87). The protocol gives no rule for Tier 2; the base card alone scored 0.87.
- **Memory.** Wave 0 hydrate: 0 hits, 2 misses. The git-ignored `.superclaude/memory/reflect/last-pass-issue-599.md` was written. The tracked write `docs/memory/reflect/deviation-patterns-issue-599.md` was skipped on purpose: it would add an untracked file under `docs/` that the plan's own checks (plan:36 and plan:158) and the story's commit step (which stages `docs/`) would trip over. Memory persistence is best-effort; the report ships without it.
- **Not produced.** `best_practice_grade` (null). Total token use was not measured; the harness reported 349,042 sub-agent tokens for the three reviewers and 216,627 for the three calibrators, and nothing for the other agents.
- **Reuse audit (advisory).** Two mirror-shape notes on the new test helpers `_region` and `_delegation_row` (same-folder neighbours exist; keep them local); neighbour search ran degraded (no codebase search tool), so no finding is blocking (`artifacts/reuse-audit.yaml`).
- **Debate artifacts.** Everything is under `adversarial/adversarial/`: `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `verification-results.md`, `return-contract.yaml`; the merged card is `adversarial/merged-output.yaml` and the reflect verdict file is `adversarial/merged-verdict.yaml`.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 58` = 0.00

No WARN: every claim is Grounded (a citation, or a command the orchestrator ran and recorded as noted above).

## Recommendations

### Recommendation R-001: Move the mutation check to Task 7 and make it an in-memory, nine-case check

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Task 2 and Task 7)
- **Change:** Delete the mutation-check bullet at plan:62; require the five new tests to take no arguments; add to Task 7 the in-memory mutation-check bullet quoted in finding M1.
- **Verifier:** After the change `grep -n "Mutation check" <plan>` finds the bullet only under Task 7; at execution `./artifacts/t7-mutation.log` lists 9 cases and exit code 0.
- **Linked deviation(s):** M1
- **Priority:** P0

### Recommendation R-002: Make the format acceptance checks satisfiable and record the baseline

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Constraints, Task 1, Task 7)
- **Change:** Apply the three wording changes quoted in finding M2 (record ruff version, exit codes and listed files in Task 1; per-file `uv run ruff format <file>` in Constraints; baseline-relative `ruff format --check` in Task 7).
- **Verifier:** Task 1's `./artifacts/baseline-pytest.md` shows the ruff version, both exit codes and the listed files; Task 7's `./artifacts/t7-checks.md` shows `ruff format --check` listing no file Task 1 did not list.
- **Linked deviation(s):** M2
- **Priority:** P0

### Recommendation R-003: Add the rule that the final verification is reported as blocked until the commit

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Constraints, Task 7)
- **Change:** Add the Constraints sentence and the named line in `./artifacts/t7-checks.md` quoted in finding M3.
- **Verifier:** `grep -n "blocked" <plan>` finds the Constraints sentence, and `./artifacts/t7-checks.md` contains `complete-suite verification: blocked until the commit`.
- **Linked deviation(s):** M3
- **Priority:** P0

### Recommendation R-004: Scope the pytest deselect constraint

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Constraints, line 22)
- **Change:** Replace the sentence "Every pytest run in this plan deselects exactly that node id ..." with the wording quoted in finding M4.
- **Verifier:** `grep -n "From the Task 7" <plan>` finds the new sentence and line 22 no longer says "Every pytest run in this plan".
- **Linked deviation(s):** M4
- **Priority:** P1

### Recommendation R-005: Name Task 2 as a dependency of Task 7

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Task 7, line 145)
- **Change:** Change the line to `Depends on: Task 2, Task 6`.
- **Verifier:** `sed -n '145p' <plan>` prints that line.
- **Linked deviation(s):** M5
- **Priority:** P2

### Recommendation R-006: Add the three missing rows to the coverage matrix

- **File:** `.dev/reflect/pre-TASK-WF-design-20261126-131233-20261126131756/artifacts/coverage-matrix.md` (this review's own artifact; no plan change)
- **Change:** Add inferred rows for source.md:92 (Task 3), :100-106 (Task 1 and Task 7) and :114 (Constraints and Task 7).
- **Verifier:** `grep -c "source.md:92" <matrix>` is at least 1, and the same for `:100-106` and `:114`.
- **Linked deviation(s):** M6
- **Priority:** P2

### Recommendation R-007: Name the requirement id under each task heading

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-131233/TASK-WF-design-20261126-131233.md` (Tasks 1 to 7)
- **Change:** Add `Requirement: R-0N` under each task heading as listed in finding T1-F1.
- **Verifier:** Re-run the coverage mapping on the plan: `coverage_pct` is 1.0 (7 of 7).
- **Linked deviation(s):** T1-F1
- **Priority:** P2


## Inferred requirements (Pass 2)

The Tier 1 pass extracted 24 inferred requirement rows from the spec. The validator re-read each quote against its cited spec line: all 24 match, none dropped, so `coverage_pct_union` (0.6774, 21 of 31 rows mapped), `unmapped_requirements_union` and `S_dev_density` (0.3226) are unchanged. The parsed-only `coverage_pct` is 0.0 because no task names an R-id. Three inferred rows are unmapped by the matrix (INF-005, INF-017, INF-022); the Tier 1 calibrator found each covered in substance (plan lines 92, 51-53, 98 and 155).

| INF id | Verbatim quote | Citation | Match result |
|--------|----------------|----------|--------------|
| INF-001 | Phase A calls `sc:workflow-protocol` with `--depth standard --handoff none` at every reflect depth. No `plan_depth`, no `Plan depth` prompt line, no change to `runner.py` route logic. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:9` | match |
| INF-002 | Contract stays `1.9.0`. The schema key `remediation_task_path` stays in the `SKILL.md` §9.1 block (`SKILL.md:829`, pinned by `test_shadow_skill_contract.py:43-50`) and in the lint allow-list (`panel_lint.py:115`). | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:10` | match |
| INF-003 | Edit surface: `src/superclaude/`, `docs/developer-guide/`, `tests/cli/reflect/`. No plugin copy of the reflect skill exists, so `make sync-dev` then `make verify-sync` is the whole mirror step. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:11` | match |
| INF-004 | Not changed (confirmed): `runner.py` (reads only `remediation_plan_path`, `runner.py:765`), `panel_lint.py`, | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:26` | match |
| INF-005 | After: the same list without `remediation_task_path`. `remediation_plan_path: str \| None = None` stays, with its default, in the same position relative to its neighbours. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:33` | match |
| INF-006 | All use keywords; only `contract.py:126` passes the removed field. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:34` | match |
| INF-007 | Signature unchanged: `(verdict: Verdict, *, reason: str, contract: dict \| None, child_rc: int) -> ReflectResult`. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:38` | match |
| INF-008 | The line keeps its other cells and `--depth standard --handoff none` in the third cell. No line is added or removed. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:47` | match |
| INF-009 | `session-memory.md:33`: `sc-reflect-protocol/SKILL.md:376` becomes `sc-reflect-protocol/SKILL.md:576` | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:48` | match |
| INF-010 | It no longer writes `reflect/handoff-*.md` files: they were retired in 6.1.0 | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:51` | match |
| INF-011 | `session-memory.md:79`, last cell: `sc-reflect-protocol/SKILL.md:262,376-378,590-600` becomes `sc-reflect-protocol/SKILL.md:262,576-598` | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:52` | match |
| INF-012 | `contract.py:124-127`: remove the kwarg line `remediation_task_path=c.get("remediation_task_path"),` | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:53` | match |
| INF-013 | `models.py:148-150`: delete the field line `remediation_task_path: str \| None = None` | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:54` | match |
| INF-014 | the docstring line becomes `    """AUTO-FIXABLE verdict with no remediation_plan_path -> terminal HALT, no apply. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:55` | match (the quote is a prefix of the line) |
| INF-015 | `_region(text, start, end)`: asserts `text.count(start) == 1` and `text.count(end) == 1` and that `start` comes first; returns the text from `start` up to `end`. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:63` | match |
| INF-016 | `_depth_tokens(text)`: returns `re.findall(r"--depth\s+([^\s`]+)", text)`. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:64` | match |
| INF-017 | the anchors exist (inside `_region` or an equivalent unique-line lookup for the row); the token list is not empty (a deleted flag cannot pass vacuously) | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:76` | match |
| INF-018 | `test_no_placeholder_depth_on_sc_workflow_lines`: for each of `_REF`, `_SKILL`, `_CMD`, for every line containing `sc:workflow`, no token from `_depth_tokens(line)` starts with `<`, `{` or `$`. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:78` | match |
| INF-019 | `plan_depth`, `Plan depth` and `--plan-depth` occur in none of `_REF`, `_SKILL`, `_CMD` | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:84` | match |
| INF-020 | the sentence `` `--depth deep` only sets the review depth `` (backticks included) occurs in `_SKILL` (`SKILL.md:363`) and in `_CMD` (`commands/reflect.md:107`). | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:85` | match |
| INF-021 | the delegation row's last cell, from `row.rstrip().rstrip("\|").rsplit("\|", 1)[-1].strip()`, equals `None; surface the report path and recommend manual planning`, and `--depth deep` is not in the row. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:86` | match (pipes as in the spec; the matrix copy shows `/`) |
| INF-022 | `test_shadow_skill_contract.py:43-50` (1.9.0 block), `test_panel_contract_lint.py`, `test_remediation_source_template.py`, `test_fix_loop.py:195-225` (both pointers; task pointer alone) | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:96` | match |
| INF-023 | Outside importers of `ReflectResult`: if the full suite shows a caller, restore the field (`models.py` one line, `contract.py` one line) and keep the comment fixes. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:113` | match |
| INF-024 | The plan should keep section 5 as an ordered step list, with step 6 (commit) marked as outside `/sc:implement`. | `.dev/tasks/to-do/TASK-WF-design-20261126-131233/source.md:128` | match |
