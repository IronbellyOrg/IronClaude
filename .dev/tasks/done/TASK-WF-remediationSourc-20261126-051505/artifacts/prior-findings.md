# Reflect report: pre-execution review of the retry-ladder plan

Plan reviewed: `.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-040738/TASK-WF-remediationSourc-20261126-040738.md` (6 tasks), against its spec `.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-040738/source.md`. In this report "plan:N" is line N of the plan, "spec:N" is line N of `source.md`, and "retry.md:N" is line N of `src/superclaude/skills/sc-implement-protocol/refs/retry.md`.

```yaml
contract_version: 1.9.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.81
citations_total: 81
citations_revalidated: 81
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

## Verdict

The plan needs revision before it is executed: 3 Blocking, 7 Medium and 6 Note findings (`finding_counts: blocking 3, label_high 0, medium 7, note 6`). The plan has a task or a constraint for every Files and Acceptance row of its spec except the type check, but the new test it describes would not catch the prose changes the spec names (M-1), one of its checks fails on a correct resolver in the observed workspace (M-2), and nothing checks types (M-3). All three are fixed by editing the plan text; no change to the implementation approach is needed. Reflect only reviews: nothing was changed.

## Run summary

| Item | Value |
|---|---|
| Mode and tier | UC-1 (pre-execution), Tier 2: the single-agent pass was forced up because the spec has no requirement IDs (parse-density guard, `coverage_degraded: parsed-sparse`) and its calibrated confidence was 0.70 |
| Reviewers | 3 read-only reviewers: analyzer (alias `sonnet`), qa (alias `haiku`), refactorer (alias `opus`); calibrated confidence 0.79, 0.86, 0.78 |
| Merge | adversarial debate, 2 rounds plus an invariant probe; convergence 1.00 (21 of 23 points unanimous); base card: reviewer 3 (score 0.8618); merged card `adversarial/merged-output.md` |
| Degradations | `calibrator_diversity: degraded` (all three model classes were reviewers); `t2_vendor_diversity: single`; executor class unresolved (`executor_class_resolved: false`, no `--executor-model`), so the anti-self-confirmation guarantee is weakened; reviewer identity unverified (reviewer 2 described itself as "OpenAI ChatGPT" though spawned on alias `haiku`) |
| Input drift | none: the input tree hash was identical at Wave 0 and Wave 5 |

## Coverage

- Parsed requirement IDs: 0. Inferred requirements: 28 (all quotes verified verbatim against their cited spec lines).
- `coverage_pct`: null (no parsed IDs). `coverage_pct_union`: 0.7143 (20 of 28 matched). `S_dev_density`: 0.2857 (mechanical value; reflect-internal).
- The 8 unmatched rows are mostly covered in substance. Five (INF-022, 023, 025, 027, 028) appear almost word for word in the plan's own `## Constraints` section (word overlap 0.97 to 1.0, `artifacts/coverage-matrix.json`). INF-026 (run `make sync-dev` and `make verify-sync`) is covered by Task 5 (plan:112); its overlap, 0.5789, fell just under the 0.6 matching threshold. INF-019 (stay within the Files list) is covered by plan:19. INF-020 (no new lint or type errors) is covered for lint by plan:140 and not for types: that is finding M-3.
- A match shows only that a task mentions the requirement, not that it satisfies it. INF-017 (spec:30) is matched to Task 6, but M-1 shows Task 6's pins do not meet it. Two matches name the wrong task (INF-007 belongs to Task 4, INF-010 to Task 6); coverage is unaffected.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | src/superclaude/skills/sc-implement-protocol/refs/retry.md: replace the sentence at line 185 (the model tier comes from the Agent call's model parameter) with one paragraph that starts with the bold words Launch alias. It states that the Agent call's model takes only opus, sonnet, haiku or fable and never a full id or a rung variable's value; on the fallback ladder the call's model is the rung's own alias; on the primary ladder it is opus for every adviser (A, B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with claude- is still launched on opus and its line 1 carries family-fallback with a reason; this never STOPs. | source.md:11 | containment: Task 1 (0.9492) |
| INF-002 | Header grammar at retry.md line 181: the line-1 header of every advice file reads model: ID family: claude-or-gpt rung: T1-or-top launch: ALIAS. The fields model, family and rung describe the pick the ladder chose; launch is the Agent model value actually passed; no header asserts the family that served the call. | source.md:12 | containment: Task 1 (0.9062) |
| INF-003 | Worked table at retry.md lines 176 to 179: change the B-column cell of all four rows from the text 1× GPT T1 to the text 1× `opus` (GPT T1 not launchable, family-fallback), written with the multiplication sign and not the letter x; leave the other columns unchanged, so the last cell of each row stays 2× `opus` and the 22-row halt regex does not match the rows. | source.md:13 | containment: Task 2 (0.7105) |
| INF-004 | retry.md lines 168 to 172: reword the primary-ladder wording and example that name T1Model01 as the GPT T1 model and a T2Model02 executor as Claude; the observed values contradict both (T1Model01 is claude-opus-5-5, T1Model02 is gpt-6.1-sol, T2Model02 is glm-5.3, T2bModel01 is gpt-6.1-terra). Draft the replacement wording first; the four rung names must stay in the file. | source.md:14 | containment: Task 3 (0.7692) |
| INF-005 | retry.md, one added sentence after the launch rule: the id prefix decides family-fallback only for primary-ladder rung ids; the fallback ladder passes the rung's own alias and the existing family reading at lines 164 to 166 is unchanged and not part of this fix. | source.md:15 | containment: Task 1 (0.7586) |
| INF-006 | plugins/superclaude/skills/sc-implement-protocol/refs/retry.md: byte-identical mirror of every change above (a test compares the two trees byte for byte). | source.md:16 | containment: Task 5 (0.7778) |
| INF-007 | src/superclaude/skills/sc-implement-protocol/SKILL.md: at line 193 widen the words every family-fallback header line of an advice-3-b.md to every family-fallback header line of an advice-N-X.md, so the final summary lists the marker from every adviser. | source.md:17 | containment: Task 1 (0.84) |
| INF-008 | plugins/superclaude/skills/sc-implement-protocol/SKILL.md: byte-identical mirror of the SKILL.md change. | source.md:18 | containment: Task 5 (0.8333) |
| INF-009 | tests/skills/test_task_workspace_lifecycle.py: update the four assertion rows at lines 598 to 604, which pin the four worked-table rows verbatim, to the new cell text in the same change. | source.md:19 | containment: Task 2 (0.9) |
| INF-010 | tests/skills/test_implement_launch_alias.py: new test file, described under Acceptance. | source.md:20 | containment: Task 1 (0.7778) |
| INF-011 | New test tests/skills/test_implement_launch_alias.py hard-codes the alias set opus, sonnet, haiku, fable and pins it to the list at docs/reference/model-aliases.md line 48, collecting the backticked alias words and dropping the words model and inherit; a comment warns not to reuse the ALIASES constant of tests/skills/test_model_alias_policy.py, which includes inherit and lacks fable. | source.md:24 | containment: Task 6 (0.7714) |
| INF-012 | The test asserts that the Model ladder section of retry.md contains the Launch alias paragraph (it must fail on today's file) and that no line of the paragraph starts with the pinned spawn-path text. | source.md:25 | containment: Task 6 (0.9048) |
| INF-013 | The test asserts that every B-column cell of the four worked-table rows is an alias or names a non-launchable pick together with family-fallback, and that no cell names a model id. | source.md:26 | containment: Task 6 (0.9474) |
| INF-014 | The test builds hermetic environments as plain dicts and never reads the real environment: the observed values, a swapped environment (T1Model01 a gpt- id and T1Model02 a claude- id), an all-claude environment, a bracket-1m suffixed environment, a partial environment (T1Model01 empty, which forces the fallback ladder) and a fallback environment with tier ids. | source.md:27 | containment: Task 6 (0.8571) |
| INF-015 | Over every environment, every executor tier and the five adviser roles (escalation 1 A and B, the critique adviser, escalation 2 first and second), the test asserts that the launch value is in the alias set and contains no opening bracket, that a non-claude- primary-ladder pick gets family-fallback and launch opus, that the fallback ladder passes the rung's own alias, and that T2Model01 is never an adviser. | source.md:28 | containment: Task 6 (0.9189) |
| INF-016 | Two negative controls must each be flagged by the same checks: a resolver that returns the raw id, and a resolver that drops the family-fallback flag. | source.md:29 | containment: Task 6 (1.0) |
| INF-017 | The test pins key phrases of the Launch alias paragraph and of the reworded lines 168 to 172, so a prose rewrite that drops the rule for opus on every adviser, or that names a GPT model as a startable spawn, cannot pass silently. | source.md:30 | containment: Task 6 (0.72) |
| INF-018 | The existing tests tests/skills/test_implement_adviser_family.py, tests/skills/test_model_alias_policy.py, tests/skills/test_implement_severity_static.py, tests/skills/test_workflow_archive.py and tests/commands/test_workflow_command.py stay green. | source.md:31 | containment: Task 6 (0.8333) |
| INF-019 | The change is limited to the files listed under Files | source.md:32 | none (best 0.25; plan Constraints section 0.5) |
| INF-020 | No new lint or type errors introduced | source.md:33 | none (best 0.2; plan Constraints section 0.2) |
| INF-021 | The new retry.md text must not start any line with the pinned spawn-path text GPT spawn path: (a test requires exactly one such line, at line 183), and must keep the backticked family-fallback reason phrase and the phrase never STOPs and never prompts the user (tests/skills/test_implement_adviser_family.py lines 73 to 85). | source.md:37 | containment: Task 1 (0.8438) |
| INF-022 | The new text must not contain the words halt, Ruling or E-HALT-QA outside the allow-listed lines (tests/skills/test_implement_severity_static.py lines 296 to 299 and 420 to 434), must not contain the string claude-gw-tier (tests/skills/test_model_alias_policy.py lines 104 to 119), and must not put a full model id after a --model or --models flag (same file, lines 164 to 173). | source.md:38 | none (best 0.5526; plan Constraints section 0.9737) |
| INF-023 | The new text must not add a fenced block with a line that begins with T and a digit and has no angle bracket (tests/skills/test_implement_severity_static.py lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is the digits 2 to 5 (tests/skills/test_workflow_archive.py lines 1042 to 1076). | source.md:39 | none (best 0.4688; plan Constraints section 1.0) |
| INF-024 | retry.md must keep the four rung names T2bModel01, T2Model02, T1Model02 and T1Model01 and must not use any T-digit-underscore-Model spelling (tests/skills/test_model_alias_policy.py lines 219 to 228). | source.md:40 | containment: Task 3 (0.6522) |
| INF-025 | No new flag, no new stop reason, no new halt reason, no change to the tier= ledger token (its value class is letters, digits and underscore), no extra adviser spawn (the cap of six stays), and no edit under .claude or .dev/issues. | source.md:41 | none (best 0.375; plan Constraints section 1.0) |
| INF-026 | Run make sync-dev and make verify-sync after editing, because the plugin tree and the project dev copies must agree; stage only the src, plugins and tests files and .dev/tasks. | source.md:42 | none (best 0.5789; plan Constraints section 0.4211) |
| INF-027 | Out of scope: the executor-tier tie when T2Model01 and T1Model02 hold the same id, and family inference from gateway ids such as claude-gw-tier2; both are separate defects. | source.md:43 | none (best 0.5263; plan Constraints section 1.0) |
| INF-028 | Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope. | source.md:44 | none (best 0.3077; plan Constraints section 1.0) |

Postscript: the evidence validator dropped no inferred row. It found one quote (INF-003) where this table had left out the spec's backticks; they are restored. The union figures above stand.

## Best-practice compliance

`best_practice_grade`: null. No external best-practice lookup runs at `--depth standard`; none is claimed.

## Gap registry

Full finding text (claim, evidence, consequence, recommendation, confidence, origin) is in `adversarial/merged-output.md`. Grades follow the review rule: Blocking only where fixing the text would change a named decision, outcome or acceptance check, or a required behaviour is absent.

| id | Grade | Gap | Evidence | Fix |
|---|---|---|---|---|
| M-1 | Blocking (Missing) | Task 6's text pins do not bind the launch rule or the reworded lines 168 to 172: `sonnet for every adviser` or an added GPT-spawn sentence still passes | spec:30; plan:43, 128 | R-001 |
| M-2 | Blocking (Decision) | "`T2Model01` is never an adviser" can only compare ids, and `T2Model01` and `T1Model02` share `gpt-6.1-sol`, so it fails on a correct resolver | plan:130-132; `.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/tier1-observation.md:9, 12` | R-002 |
| M-3 | Blocking (Missing) | no step checks types although spec:33 names type errors; mypy is configured but run by no gate | spec:33; plan:140; `pyproject.toml:209-217` | R-003 |
| M-4 | Medium | the pinned "paragraph" is two paragraphs and its end is never stated | plan:43, 45, 128 | R-004 |
| M-5 | Medium | the neither-family and GPT-executor selection rules are missing from Task 3 and the Task 6 resolver | retry.md:168-169; plan:82, 130 | R-005 |
| M-6 | Medium | the header has no content when no model is reachable | plan:43, 45 | R-006 |
| M-7 | Medium | two readings for fallback-ladder adviser B across plan:43, 45, 132 | plan:43, 45, 64-67, 132 | R-007 |
| M-8 | Medium | the clause "on `T1Model02`, adviser A on `T1Model01`" at retry.md:172 is not banned | retry.md:172; plan:89 | R-008 |
| M-9 | Medium | Task 6's header check builds its own string and cannot fail | plan:132 | R-009 |
| M-10 | Medium | the worked-table parser has no row-count guard | retry.md:172-179; plan:129 | R-010 |
| N-1 to N-6 | Note | `.claude/` wording, Task 6 dependency list, three wrong labels, old test helper, a test missing from the run lists, a baseline for the red check | see `adversarial/merged-output.md` | R-011 |

## Recommendations

Each recommendation names the plan task to edit (all in `.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-040738/TASK-WF-remediationSourc-20261126-040738.md`), the change, and the check that confirms it.

### Recommendation R-001: Bind the Task 6 pins to the rule and to the reworded lines

- **File:** plan, Task 3 and Task 6
- **Change:** pin the exact phrase "is `opus` for every adviser"; add a count check that `sonnet`, `haiku` and `fable` occur in the Launch alias block only inside the "takes only ..." sentence; have Task 3 fix one exact sentence for lines 168 to 172 (every primary-ladder adviser is launched on `opus`; a pick that is not `claude-` carries `family-fallback`), embedded as a literal in the test and pinned between the `**Escalation rule.**` line (retry.md:166) and the lead-in "Worked example with the fallback ladder:" (each anchor once); assert no model-id literal in the block and that span; pin retry.md:181 (no "strongest reachable model", contains `opus`); mutation checks that change one named occurrence and name the pin that failed.
- **Verifier:** each mutation fails exactly its pin; the pins pass on the changed retry.md and fail on `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/retry.md`.
- **Linked finding(s):** M-1
- **Priority:** P0

### Recommendation R-002: Check the source variable, not the id

- **File:** plan, Task 6 (resolver bullet and sweep bullet)
- **Change:** add a `source` field to each resolver record; assert that no record's `source` is `T2Model01`; add a third negative control that picks `T2Model01` as "one rung up" for a `T2Model02` executor.
- **Verifier:** the sweep passes in the observed environment (`T2Model01` and `T1Model02` both `gpt-6.1-sol`) and the third control is flagged.
- **Linked finding(s):** M-2
- **Priority:** P0

### Recommendation R-003: Add a type check to Task 6

- **File:** plan, Task 6 acceptance criteria
- **Change:** add `uv run mypy tests/skills/test_implement_launch_alias.py` with no new diagnostics; type the record and check any regex match is not None before use.
- **Verifier:** the mypy command exits 0 on the new file. [INFERRED] whether mypy is clean on the existing tests; not checked.
- **Linked finding(s):** M-3
- **Priority:** P0

### Recommendation R-004: Name the pinned block

- **File:** plan, Task 6 "Paragraph" bullet
- **Change:** define the block as the lines from `**Launch alias.**` to the `### Cost and caps` heading and apply the `launch:` pin and the `GPT spawn path:` exclusion to it.
- **Verifier:** the pin passes on the changed retry.md and fails on the pre-change file.
- **Linked finding(s):** M-4
- **Priority:** P1

### Recommendation R-005: Add the missing selection rules

- **File:** plan, Task 3 (rule 2) and Task 6 (resolver bullet)
- **Change:** add the retry.md:168 neither-family rule and the retry.md:169 GPT-executor rule, and give each environment and executor tier an explicit expected pick and `family_fallback` value (observed environment, executor on `T2Model02`: adviser A = `T1Model01`, adviser B = the `gpt-` T1 id).
- **Verifier:** the sweep includes a glm executor and a GPT executor with those expected picks.
- **Linked finding(s):** M-5
- **Priority:** P1

### Recommendation R-006: Define the no-model header

- **File:** plan, Task 1 and Task 6
- **Change:** add one sentence giving the header form when no model is reachable (for example `model: none family: none rung: <T1|top>` plus `family-fallback`), and check headers by a token-set rule (keys exactly `model`, `family`, `rung`, `launch`, optionally `family-fallback`).
- **Verifier:** both the normal and the no-pick header pass the check.
- **Linked finding(s):** M-6
- **Priority:** P1

### Recommendation R-007: Make fallback-ladder adviser B consistent

- **File:** plan, Task 1 text (plan:45), Task 6 resolver rule (plan:130) and sweep assertion (plan:132)
- **Change:** change the three together: on the fallback ladder adviser B is launched on `opus` with `family-fallback` when its pick is not `claude-`; the "rung's own alias" assertion applies to picks that are fallback rungs.
- **Verifier:** the resolver output for the fallback and partial environments matches the four Task 2 rows (plan:64-67).
- **Linked finding(s):** M-7
- **Priority:** P1

### Recommendation R-008: Ban the third stale clause

- **File:** plan, Task 3 acceptance (plan:89) and Task 6 absent-phrase pin
- **Change:** add "on `T1Model02`, adviser A on `T1Model01`" to the banned phrases.
- **Verifier:** a search of retry.md for the clause returns nothing.
- **Linked finding(s):** M-8
- **Priority:** P1

### Recommendation R-009: Run the header check on the documented text

- **File:** plan, Task 6 header check (plan:132)
- **Change:** assert the token-set rule on the header form documented in the Launch alias block of retry.md, not on a string the test builds.
- **Verifier:** removing `launch:` from the documented form fails the check.
- **Linked finding(s):** M-9
- **Priority:** P1

### Recommendation R-010: Guard the worked-table parse

- **File:** plan, Task 6 "Worked table" bullet (plan:129)
- **Change:** assert exactly 4 rows with first cells `haiku`, `sonnet`, `opus (known)` and `unknown`, and define the parenthetical test.
- **Verifier:** dropping a row from a copy of retry.md fails the check.
- **Linked finding(s):** M-10
- **Priority:** P1

### Recommendation R-011: Correct the plan's labels and lists

- **File:** plan (Constraints, Task 3, Task 5, Task 6)
- **Change:** reword "Edit nothing under `.claude/`" to "stage and hand-edit nothing under `.claude/`"; add Tasks 4 and 5 to Task 6's "Depends on"; replace "pinned line 183" with "pinned text", complete the forbidden-word list, and name the lines 168 to 172 span by its anchors; add `tests/skills/test_review_severity_rule.py` to the Task 5 and Task 6 runs; pin the red-check baseline to the merge base with `origin/integration`.
- **Verifier:** re-read the plan's Constraints and Tasks 3, 5 and 6 and confirm no sentence conflicts.
- **Linked finding(s):** N-1 to N-6
- **Priority:** P2

## Tier 2 record and accepted risk

- Reviewer cards: `reviewer-cards/reviewer-1-card.md`, `reviewer-2-card.md`, `reviewer-3-card.md`, each with its blind calibration (`*-calibration.md`). The debate is in `adversarial/adversarial/debate-transcript.md`; the invariant probe (17 findings) is in `adversarial/adversarial/invariant-probe.md`.
- One close call: the missing type check (M-3) was graded Blocking by 2 of 3 advocates because spec:33 names type errors and no plan step covers them; the third held Medium because no repo gate runs mypy. The grade stands on the spec's wording.
- Accepted risk (invariant INV-001): the new test's resolver, environments and sweep never read the prose, so only the text pins can catch a prose rewrite. The spec itself says the test can pin only the instruction text (spec:7). A controlled launch per alias remains a follow-up.
- Not checked: the state of `.claude/` in this worktree (gitignored), and whether mypy is clean on existing tests.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 81` = 0.01
