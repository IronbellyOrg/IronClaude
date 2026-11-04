# Reflect report — UC-1 pre-execution check of TASK-WF-refactorIronClau-20261102-162730

```yaml
contract_version: 1.8.0
status: partial            # the adversarial merge returned partial: convergence BLOCKED_BY_INVARIANTS (INV-005) and one post-merge wording contradiction; no citation was dropped
mode: pre
tier_reached: 2
confidence_calibrated: 0.80   # mean of the three blind-calibrated Tier-2 cards (0.80, 0.76, 0.83); Tier-1 card was 0.71
citations_total: 108
citations_revalidated: 108
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread   # stricter than required: every citation was re-read
coverage_degraded: parsed-sparse
plan_verdict: revise-before-execution   # 1 high, 3 medium, 10 low deviations; 0 regressions
```

## Verdict

The plan covers every obligation in its spec except one: "every tracked file that encodes ... git worktree add" (source.md:1). The spec's own grep cannot see list-argument calls, so `scripts/eval_runner.py` creates a never-removed worktree beside the repo (scripts/eval_runner.py:138, :143) that no task classifies or changes. Three medium gaps also need fixing before execution:
- Task 3 keeps pre-PR checks that still reach upstream (CLAUDE.md:64, :66).
- More list-argument calls break Task 1's count check.
- The plan assumes an `upstream` remote that this repository does not have (CLAUDE.md:41).

Ten low findings are wording, labels or extra checks. No requirement is contradicted, so there is no Regression.

How the verdict was reached:
- Tier 2: three read-only reviewers on different model classes, sonnet (analyzer lens), the haiku slot (glm-5.3, qa lens) and opus (refactorer lens), with blind-calibrated confidence 0.80, 0.76 and 0.83. Merged by `/sc:adversarial` at standard depth: base reviewer-1, 13 of 13 debate points agreed by majority.
- The merge itself is partial. The invariant probe found one HIGH unaddressed item (INV-005, the eval_runner.py gap), and the post-merge re-scan found one wording contradiction in finding R1-2's headline. Both are recorded in `adversarial/return-contract.yaml`.
- Tier 1 was a single inline card with calibrated C 0.71. It escalated because the spec has no requirement IDs (coverage_degraded: parsed-sparse) and the plan spans three domains (docs, config, tests).

Artifacts (paths relative to this report's directory): `t1-card.md`, `artifacts/coverage-matrix.json`, `artifacts/pass2-inferred.yaml`, `artifacts/tier_decision.yaml`, `reviewer-cards/`, `adversarial/merged-findings.md`, `adversarial/merged-verdict.yaml`, `adversarial/adversarial/` (diff analysis, debate transcript, invariant probe, base selection, refactor plan, merge log), `audit.log`.

## Inferred requirements (Pass 2)

Pass 1 found 0 labeled requirement IDs. Pass 2 (requirements-analyst agent) inferred 11 quote-pinned rows. All cite `.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md:1`, the spec's only line. Match is the deterministic containment rule (threshold 0.6); "content-level" is the qa reviewer's and the merge's verdict on substance.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "Refactor IronClaude to Orca's default worktree paths" | source.md:1 | containment, Task 1 (0.857) |
| INF-002 | "replace the .dev/worktrees rule in CLAUDE.md" | source.md:1 | containment, Task 2 (1.0) |
| INF-003 | "every tracked file that encodes .dev/worktrees or git worktree add" | source.md:1 | containment, Task 1 (0.75); content-level PARTIAL (D-001, D-003) |
| INF-004 | "(git grep -E '\.dev/worktrees\|git worktree add' -- ':!.dev')" (the backslash before the pipe is a Markdown table escape; the source has a bare pipe) | source.md:1 | containment, Task 1 (1.0) |
| INF-005 | "Classify each hit as project worktree (move to Orca-created worktrees at Orca's default location) or internal temporary checkout used by a CLI or test (keep working without Orca)." | source.md:1 | containment, Task 1 (0.842); plan adds a third class (D-006) |
| INF-006 | "project worktree (move to Orca-created worktrees at Orca's default location)" | source.md:1 | containment, Task 2 (0.889) |
| INF-007 | "internal temporary checkout used by a CLI or test (keep working without Orca)" | source.md:1 | containment, Task 1 (0.889); proved only by "unchanged" (D-008) |
| INF-008 | "Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with." | source.md:1 | containment, Task 3 (0.9) |
| INF-009 | "Source of truth is src/superclaude" | source.md:1 | containment, Task 5 (1.0) |
| INF-010 | "run make sync-dev" | source.md:1 | containment, Task 6 (1.0) |
| INF-011 | "never stage .claude mirrors" | source.md:1 | none lexically (best Task 3, 0.5); content-level COVERED by plan line 20 (Constraints: never stage a `.claude/` path except `.claude/settings.json`) and the Task 6 and Task 7 staging criteria (plan lines 122, 136) |

Coverage: coverage_pct null (no parsed IDs), coverage_pct_union 0.9091 (10 of 11 lexical), S_dev_density 0.0909. Content level: 10 covered and 1 partial (INF-003).

## Deviations

"Plan" below means `.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md`. These are deviations of the PROPOSED plan from its spec, found before execution. Classes are from the 4-category taxonomy. Merged finding ids are in brackets.

### Deviation D-001: The spec's grep misses scripts/eval_runner.py, and no task handles it [M-1]

- **Location:** scripts/eval_runner.py:138-147
- **Mapped tasklist item:** unmapped (Task 1 inventory and Task 7 residual check cannot see it)
- **Spec section:** source.md:1, INF-003 "every tracked file that encodes ... git worktree add"
- **Evidence:** `worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"` (scripts/eval_runner.py:138) and `["git", "worktree", "add", str(worktree_path), "master"],` (scripts/eval_runner.py:143). The `subprocess.run` result is ignored and there is no removal (scripts/eval_runner.py:142-147). Plan line 57 limits the exception to checkouts a CLI or test "creates and removes itself"; plan line 33 says "Use exactly these classes and assignments".
- **Classification:** drift
- **Classification rationale:** A real tracked worktree creator is outside the plan with no recorded reason. It fits neither the project-worktree class nor the internal-checkout exception. It contradicts no acceptance criterion, so it is not a regression. Reviewer 3 (R3-F1), X-002 consensus 97%, invariant INV-005 (HIGH).
- **Default remediation:** Add a task that classifies scripts/eval_runner.py and changes it to either create-and-remove its own temporary checkout or use an Orca-created worktree, and extend Task 7's residual check with a list-argument search.

### Deviation D-002: Task 3 keeps two pre-PR checks that still act on upstream [R1-1]

- **Location:** CLAUDE.md:64, CLAUDE.md:66
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1, INF-008 "SuperClaude upstream is never pushed to or interacted with"
- **Evidence:** CLAUDE.md:64 runs `gh repo view --json nameWithOwner -q .nameWithOwner` with no repo argument and says what to do "if it prints the upstream parent". CLAUDE.md:66 says "If it shows the wrong owner, close it immediately and reopen with `--repo IronbellyOrg/IronClaude`." Plan line 78 keeps the pre-PR checks and says only "Edit them only where they contradict the rules above."
- **Classification:** drift
- **Classification rationale:** The new unconditional rule and the kept checks would contradict each other inside one section, and no acceptance criterion of Task 3 names either line. After check 3 is removed, nothing says how a misrouted PR is recovered (INV-008). `gh repo view` takes a positional repo, so "--repo on every gh call that accepts it" does not cover it (INV-009). All three reviewers agreed; 97%.
- **Default remediation:** Name both checks in Task 3. Rewrite check 1 to use `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude`. Rewrite check 3 as "stop, report the URL, the user closes it", matching src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:222. Add an acceptance criterion that `grep -n 'close it immediately' CLAUDE.md` prints nothing.

### Deviation D-003: More list-argument worktree calls exist, which breaks Task 1's count check [M-2]

- **Location:** tests/unit/test_ccsession_tag.py:1858, :1912; tests/troubleshoot/backtest/test_git_replay_unit.py:34; src/superclaude/cli/reflect/config.py:202; tests/troubleshoot/backtest/git_replay.py:191; tests/skills/test_implement_retry_revert.py:614, :1054; tests/cli/reflect/test_isolate_reviewers_cli.py:147
- **Mapped tasklist item:** Task 1 (acceptance at plan line 42), Task 7
- **Spec section:** source.md:1, INF-003
- **Evidence:** `git grep -n -E '"worktree",\s*"add"' -- ':!.dev'` (run by the orchestrator 2026-11-02) prints 9 lines: the 8 above plus scripts/eval_runner.py:143 (D-001). Plan line 42 requires per-file counts that sum to the live `git grep -c` total of the spec's pattern.
- **Classification:** drift
- **Classification rationale:** These are internal temporary checkouts in tests and the reflect CLI, so they need no change. For example, tests/unit/test_ccsession_tag.py:1850-1858 builds its repo in pytest `tmp_path`, and tests/troubleshoot/backtest/test_git_replay_unit.py:28-34 only inspects mocked arguments. But they are uncounted, and adding them under the current acceptance rule breaks the sum (INV-003, INV-004).
- **Default remediation:** Run a second list-argument search in Task 1 with its own total, and give each new file a class and a reason.

### Deviation D-004: The plan assumes an `upstream` remote that does not exist [M-4]

- **Location:** CLAUDE.md:41; plan lines 73 and 76
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1, INF-008
- **Evidence:** `git remote -v` prints only `origin  https://github.com/IronbellyOrg/IronClaude` (orchestrator, 2026-11-02). CLAUDE.md:41 says "`upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent)." pyproject.toml:64-67 still points at SuperClaude-Org/SuperClaude_Framework.
- **Classification:** drift
- **Classification rationale:** A rule keyed to a remote named `upstream` does not cover how this repository actually reaches upstream. The plan's guard "Until `orca worktree current --json` shows the fork's project id" (plan line 76) may never lift if Orca derives the project id from those URLs (INV-001).
- **Default remediation:** Word Task 3's rule as "no remote, URL or tool call that resolves to SuperClaude-Org/SuperClaude_Framework", and record the source of Orca's project id as unverified.
- **[INFERRED] notes:** [INFERRED] That Orca takes its project id from the pyproject.toml or package.json URLs is a hypothesis; it was not checked against Orca's source.

### Deviation D-005: The static upstream issue link vs Task 3's "no ... link" wording [R1-5]

- **Location:** CLAUDE.md:251; plan line 73
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1, INF-008
- **Evidence:** CLAUDE.md:251 links `https://github.com/SuperClaude-Org/SuperClaude_Framework/issues/419`; plan line 73 says "no tool call or link (gh, git or Orca) that resolves to it"; plan line 82's acceptance names only Orca `--issue`/`--pr` linking.
- **Classification:** drift
- **Classification rationale:** Read literally, the new rule bans a link the same file keeps (2-1 vote, 62%). Upstream URLs also sit in deliberate negative test fixtures (tests/pr_submit/test_pre_pr_checks.py:37, :82), so a literal ban cannot be met without weakening tests (INV-011).
- **Default remediation:** Narrow plan line 73 to "no tool call, and no gh or Orca link flag", and state that static references in docs and test fixtures are out of scope.

### Deviation D-006: A third class "Historical record" for POST-REFLECT-TASK.md [R1-2]

- **Location:** plan line 37; POST-REFLECT-TASK.md:6
- **Mapped tasklist item:** Task 1
- **Spec section:** source.md:1, INF-005 (two classes)
- **Evidence:** Plan line 37 adds "Historical record, keep unchanged" for POST-REFLECT-TASK.md (79 hits). POST-REFLECT-TASK.md:6 reads `status: "🔴 Blocked"`.
- **Classification:** necessary
- **Classification rationale:** Forcing those lines into the source's two classes would mean rewriting a dated execution record. The plan states its reason inline, and the change contradicts no requirement. It still covers 79 of 108 hits, so the user should see it.
- **Default remediation:** Keep the class, note in Task 1 that the file is Blocked and its paths are intentionally stale, and report the class first in the inventory summary.

### Deviation D-007: Task 1 labels the .gitignore entry "rewrite" while Task 4 keeps it [R1-3]

- **Location:** plan lines 35 and 89; .gitignore:242
- **Mapped tasklist item:** Task 1, Task 4
- **Spec section:** source.md:1, INF-002
- **Evidence:** Plan line 35 lists the `.dev/worktrees/` entry under "Project worktree, rewrite to Orca's default location"; plan line 89 says "Keep the `.dev/worktrees/` entry itself."
- **Classification:** necessary
- **Classification rationale:** Keeping the ignore entry is a deliberate safety guard, so only the inventory label is wrong.
- **Default remediation:** Change the Task 1 row's action to "rewrite comment only; keep entry as a retired-path guard (see Task 4)".

### Deviation D-008: "Keeps working without Orca" is proved only by "unchanged" [R1-4]

- **Location:** plan line 135; tests/troubleshoot/backtest/test_git_replay_integration.py:56-68; .github/workflows/test.yml:17
- **Mapped tasklist item:** Task 7
- **Spec section:** source.md:1, INF-007
- **Evidence:** Plan line 135 checks only that the internal-checkout files show no change. test_git_replay_integration.py skips the whole module when pinned commits are missing (lines 56-68), and CI checks out with `actions/checkout@v4` and no `fetch-depth` (.github/workflows/test.yml:17).
- **Classification:** drift
- **Classification rationale:** The obligation is "keep working", and the check offered cannot tell working from broken. A plain pytest run can also pass by skipping: shallow clones skip the replay module, and tests/skills/test_implement_retry_revert.py:357 skips one test when run as root (INV-006).
- **Default remediation:** Run the three internal-checkout test files with `-rs` in Task 7, save the output, and require zero skips or a recorded reason plus a rerun in a full-depth, non-root checkout.

### Deviation D-009: Fetch/pull ban and Orca project-id note go beyond the spec's words [R1-6]

- **Location:** plan lines 73 and 76
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1, INF-008
- **Evidence:** source.md:1 "SuperClaude upstream is never pushed to or interacted with."; plan line 76 adds a dated Orca project-id observation.
- **Classification:** authorized
- **Classification rationale:** Fetch and pull are interaction, so banning them is a literal reading (95%). The dated Orca bullet is backed by the user's memory entry "Never touch SuperClaude upstream — no push, PR, comment or Orca link to SuperClaude-Org".
- **Default remediation:** None.

### Deviation D-010: Orca flags used without being in the confirmed list [M-9]

- **Location:** plan lines 23, 54, 56, 76
- **Mapped tasklist item:** Constraints, Task 2, Task 3
- **Spec section:** n/a (plan-internal consistency)
- **Evidence:** Plan line 23 confirms `orca worktree create`, `list`, `current` and `rm` and says to check `--help` before naming other flags; plan lines 54, 56 and 76 name `--json`, `--issue` and `--pr`. `orca worktree create --help` (run by the orchestrator 2026-11-02) lists `--json`, `--issue` and `--pr`, and `orca worktree current --json` ran successfully in the same session and returned this worktree's JSON record.
- **Classification:** drift
- **Classification rationale:** A plan-internal inconsistency. The flags exist, so the impact is wording only.
- **Default remediation:** Add the three flags to the Constraint's confirmed list.

### Deviation D-011: Task 6 skips the contract test for the files Task 5 edits [M-10]

- **Location:** tests/skills/test_sc_recommend_routing_contract.py:27, :29, :130; plan line 116
- **Mapped tasklist item:** Task 6
- **Spec section:** source.md:1, INF-009
- **Evidence:** The test reads src/superclaude/skills/sc-recommend/SKILL.md (line 27), src/superclaude/commands/recommend.md (line 29) and refs/surface-enumeration.md (line 130); plan line 116 runs only tests/commands/test_routing_plugin_parity.py and tests/recommend/.
- **Classification:** drift
- **Classification rationale:** A missing check on edited files. The test pins no `worktree` or `.dev/` string (validator Grep).
- **[INFERRED] notes:** [INFERRED] Because the pinned strings do not overlap the planned edits, the test will most likely pass after Task 5.
- **Default remediation:** Add the test to Task 6's pytest command.

### Deviation D-012: The post-release tag checkout does not meet the create-and-remove exception [M-11]

- **Location:** src/superclaude/skills/sc-post-release-protocol/SKILL.md:91; plan line 57
- **Mapped tasklist item:** Task 1, Task 2
- **Spec section:** source.md:1, INF-007
- **Evidence:** SKILL.md:91 offers "a `git worktree add` / `git archive` checkout of the tag" with no location and no removal; plan line 57 defines the exception as checkouts a CLI or test "creates and removes itself".
- **Classification:** drift
- **Classification rationale:** The plan's own exception definition does not fit one of the four cases it names.
- **Default remediation:** Describe it in Task 2 as an optional read-only tag checkout removed after the scan, or reclassify it in Task 1.

### Deviation D-013: Two live checkouts remain at the retired location [M-12a]

- **Location:** /home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates and /home/coder/workspaces/IronClaude/.dev/worktrees/markdownlint-issue-body-files (`git worktree list`)
- **Mapped tasklist item:** Task 2 (unaddressed)
- **Spec section:** source.md:1, INF-006
- **Evidence:** `git worktree list` (orchestrator, re-run 2026-11-02T18:52Z) shows `/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates  dbfef216 [feat/issue-body-templates]` and `/home/coder/workspaces/IronClaude/.dev/worktrees/markdownlint-issue-body-files  acee54eb [fix/markdownlint-issue-body-files]`. The second was found by the evidence validator after the 18:38Z spot-check.
- **Classification:** drift
- **Classification rationale:** The new rule retires the location, but the plan says nothing about checkouts already there (INV-002).
- **Default remediation:** Add one sentence to Task 2's rule on existing retired-location checkouts (for example: leave them until their branch merges, never create new ones). Do not move or remove them as part of this plan.

### Deviation D-014: A runbook cites a `.claude/worktrees/` path neither grep covers [M-12b]

- **Location:** docs/swarm/runbook.md:34
- **Mapped tasklist item:** unmapped
- **Spec section:** n/a (outside the spec's grep)
- **Evidence:** docs/swarm/runbook.md:34 reads "- The fork's CLAUDE.md (`/config/workspace/IronClaude/.claude/worktrees/BareReview/CLAUDE.md`)".
- **Classification:** drift
- **Classification rationale:** An old worktree path outside the hit set. It is a documentation example, not a rule (INV-014).
- **Default remediation:** Note it in Task 1 as out of scope, or fix it as a one-line doc edit.

## Inferred-claim audit

- `citations_inferred: 2` (D-004 note on the source of Orca's project id; D-011 note that the contract test will most likely pass)
- Inferred-fraction: `2 / 108` = 0.02
- Evidence-validator: full re-read of all 108 citations, 0 dropped, 0 INF rows dropped. Its zero-drop self-audit lists every range it read. Its accuracy notes were applied before finalizing: D-003 line count, the D-004 quote, D-008, D-010, D-011 and D-013 (second checkout), and the INF-011 citation.
- Shell-only evidence (not re-readable, partially cross-checked by the validator from git config files): `git remote -v`, `git worktree list`, the list-argument `git grep`, `orca worktree create --help`.

## Recommendations

All recommendations are edits to the plan file (`.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md`). This check is advisory: it does not edit the plan.

### Recommendation R-001: Add a task for scripts/eval_runner.py and the list-argument search

- **File:** plan Task 1, Task 2 and Task 7 (or a new task before Task 7)
- **Change:** Classify scripts/eval_runner.py explicitly. Change it so its checkout is either created and removed by the script (internal temporary checkout) or an Orca-created worktree. Add the search `git grep -n -E '"worktree",\s*"add"' -- ':!.dev'` to Task 1 with its own total and to Task 7's residual check.
- **Verifier:** Task 7's saved residual output contains no unclassified line from either search; `grep -n "worktree" scripts/eval_runner.py` shows the chosen create/remove or Orca path.
- **Linked deviation(s):** D-001, D-003
- **Priority:** P0

### Recommendation R-002: Name and rewrite both pre-PR checks in Task 3

- **File:** plan Task 3
- **Change:** Name CLAUDE.md check 1 (bare `gh repo view`) and check 3 ("close it immediately and reopen"). Rewrite check 1 with `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude`. Rewrite check 3 as "stop, report the URL; the user closes the upstream PR". List the allowed forms for commands that take a positional repo.
- **Verifier:** `grep -n 'close it immediately' CLAUDE.md` prints nothing, and every `gh` line in the fork-rule section names IronbellyOrg/IronClaude.
- **Linked deviation(s):** D-002
- **Priority:** P1

### Recommendation R-003: Word the upstream rule without depending on a remote named `upstream`

- **File:** plan Task 3
- **Change:** Forbid any remote, URL or tool call that resolves to SuperClaude-Org/SuperClaude_Framework; note that this repository has only `origin`, and that the source of Orca's project id is unverified.
- **Verifier:** The rewritten section's prohibitions do not depend on a remote being named `upstream`; `git remote -v` output is quoted in the task's artifact.
- **Linked deviation(s):** D-004
- **Priority:** P1

### Recommendation R-004: Prove internal checkouts still work, with no silent skips

- **File:** plan Task 7
- **Change:** Run `uv run pytest tests/cli/reflect/test_isolate_reviewers_cli.py tests/troubleshoot/backtest/test_git_replay_integration.py tests/skills/test_implement_retry_revert.py -v -rs` and save it under ./artifacts/; require zero skips, or a recorded reason and a rerun in a full-depth, non-root checkout.
- **Verifier:** The saved output shows those files passing with no SKIPPED line, or a recorded reason.
- **Linked deviation(s):** D-008
- **Priority:** P2

### Recommendation R-005: Narrow "no ... link" to tool calls and link flags

- **File:** plan Task 3 (line 73 wording)
- **Change:** Say "no tool call, and no gh or Orca link flag, that resolves to it"; state that static references in docs and test fixtures are out of scope; decide CLAUDE.md:251 explicitly.
- **Verifier:** `grep -n 'SuperClaude-Org' CLAUDE.md`; every remaining hit is either a prohibition or the decided :251 line.
- **Linked deviation(s):** D-005
- **Priority:** P2

### Recommendation R-006: Fix the small plan inconsistencies

- **File:** plan Constraints, Task 1, Task 2, Task 6
- **Change:** Add `--json`, `--issue`, `--pr` to the confirmed Orca list (D-010); relabel the .gitignore row "rewrite comment only; keep entry" (D-007); describe the post-release tag checkout as optional and removed after the scan (D-012); add tests/skills/test_sc_recommend_routing_contract.py to Task 6's pytest command (D-011); say in Task 2 what happens to existing retired-location checkouts (D-013); note docs/swarm/runbook.md:34 (D-014); note the third class and the Blocked status in Task 1 (D-006).
- **Verifier:** Re-run `/sc:reflect --mode pre` on the revised plan; these findings no longer appear.
- **Linked deviation(s):** D-006, D-007, D-010, D-011, D-012, D-013, D-014
- **Priority:** P2
