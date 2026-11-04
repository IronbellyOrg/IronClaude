<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1, sonnet, analyzer) -->
<!-- Merge date: 2026-11-02T18:41:04Z -->

```yaml
reviewer: merged
base: variant-1
findings:
  - id: R1-1
    headline: "Task 3 leaves two pre-PR check lines that contradict the new 'no interaction, no exceptions' rule, and no acceptance criterion catches them"
    location: "CLAUDE.md:64, CLAUDE.md:66; plan lines 73, 75, 78, 80-83"
    classification: drift
    severity: medium
    evidence: |
      CLAUDE.md:64: "`gh repo view --json nameWithOwner -q .nameWithOwner` must print `IronbellyOrg/IronClaude`; if it prints the upstream parent, run `gh repo set-default IronbellyOrg/IronClaude` first"
      CLAUDE.md:66: "If it shows the wrong owner, close it immediately and reopen with `--repo IronbellyOrg/IronClaude`."
      Plan line 73: "no tool call or link (gh, git or Orca) that resolves to it"
      Plan line 78: "the pre-PR checks ... stay. Edit them only where they contradict the rules above."
    rationale: |
      Plan line 78 permits edits only where a line contradicts the new rules, but it never names the lines that do; the unqualified `gh repo view` can resolve to upstream, and closing a misrouted PR is an action on upstream, so the finished section would break its own unconditional rule.
      Recovery gap (INV-008): after check 3 is removed there is no permitted recovery for a PR opened on upstream by mistake. The rewrite must say the agent stops, reports the URL, and the user closes the PR. This matches src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:222, which already halts on a misrouted URL (INV-007, addressed).
      gh-flag gap (INV-009): "--repo on every gh call that accepts it" does not cover `gh repo view` (takes a positional repo) or `gh api repos/{owner}/{repo}` (fills in the default repo); tests/pr_submit/test_static_grep.py:616 pins the bare `gh repo view` fallback.
    recommendation: |
      In Task 3, name pre-PR check 1 (`gh repo view` without an explicit repo) and check 3 (closing a PR on upstream). Rewrite check 1 to read the remote with `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude`. Rewrite check 3 to say: stop, report the URL to the user, and take no action on the upstream PR; the user closes it. Add an acceptance criterion: `grep -n 'close it immediately' CLAUDE.md` prints nothing, and every `gh` line in the section carries `--repo IronbellyOrg/IronClaude` or an explicit repo argument.
      The acceptance criterion names the exact allowed forms for `gh repo view` and `gh api repos/{owner}/{repo}`, rather than relying on "--repo on every gh call that accepts it".
    provenance: "Variant 1 R1-1 (base) + INV-008, INV-009 (INV-007 addressed); Variant 3 R3-F2 considered as alternative, not adopted; Change #3"
  - id: M-1
    headline: "The hit search misses scripts/eval_runner.py, which creates a persistent worktree outside Orca that fits neither plan class and that no task edits"
    location: "scripts/eval_runner.py:138-147; plan lines 19, 33, 57, 134; source.md:1"
    classification: drift
    severity: high
    evidence: |
      scripts/eval_runner.py:138: `worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"`
      scripts/eval_runner.py:143: `["git", "worktree", "add", str(worktree_path), "master"],`
      scripts/eval_runner.py:142-147: the `subprocess.run` return code is ignored; the script never removes the worktree.
      Plan line 19: the hit set is the output of `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'`, which cannot match a list-argument call.
      Plan line 57: "creates and removes itself"
      Plan line 33: "Use exactly these classes"
      Plan line 134: Task 7 re-runs only the first grep.
    rationale: |
      The spec's grep (plan line 19) cannot see this call, it fits neither plan class, and no task edits it, so the plan leaves a scope gap against source.md:1 "every tracked file". X-002 consensus 97% (debate-transcript.md); INV-005 (HIGH, UNADDRESSED) blocks convergence.
    recommendation: |
      Add a task (or extend Task 1 and Task 2) that classifies scripts/eval_runner.py explicitly: either rewrite it to create and remove its own temporary checkout (internal temporary checkout) or route it to an Orca-created worktree. Extend Task 7's residual check with the list-argument search.
    provenance: "Variant 3 R3-F1 + INV-005, Change #1"
  - id: M-2
    headline: "List-argument `worktree add` calls also appear outside the 17 inventoried files and on uncounted lines inside them, which breaks Task 1's count accounting"
    location: "tests/unit/test_ccsession_tag.py:1858, :1912; tests/troubleshoot/backtest/test_git_replay_unit.py:34; src/superclaude/cli/reflect/config.py:202; tests/troubleshoot/backtest/git_replay.py:191; tests/skills/test_implement_retry_revert.py:614, :1054; tests/cli/reflect/test_isolate_reviewers_cli.py:147; plan line 42"
    classification: drift
    severity: medium
    evidence: |
      Outside the 17 files: tests/unit/test_ccsession_tag.py:1858, :1912; tests/troubleshoot/backtest/test_git_replay_unit.py:34.
      Uncounted lines in listed files: src/superclaude/cli/reflect/config.py:202; tests/troubleshoot/backtest/git_replay.py:191; tests/skills/test_implement_retry_revert.py:614, :1054; tests/cli/reflect/test_isolate_reviewers_cli.py:147.
      Plan line 42: Task 1's acceptance requires counts summing to the live `git grep -c` total.
    rationale: |
      scripts/eval_runner.py is not the only worktree creation the grep misses (INV-003), and a row added from a second search breaks the required sum unless it carries its own total (INV-004).
    recommendation: |
      Task 1 runs a second search `git grep -n -E '"worktree",\s*"add"|worktree", "add"' -- ':!.dev'` and keeps a separate total for it; each new file gets a class and a reason.
    provenance: "INV-003 + INV-004, Change #2"
  - id: R1-2
    headline: "The third class 'Historical record' is a necessary deviation from the source's two classes. The plan's description of POST-REFLECT-TASK.md as a finished past record is incomplete."
    location: "plan lines 25, 37; POST-REFLECT-TASK.md:6, 576"
    classification: necessary
    severity: low
    evidence: |
      Plan line 37: "It is an MDTM task file dated 2026-06-22 whose paths ... record where that past run executed."
      POST-REFLECT-TASK.md:6: `status: "🔴 Blocked"`
      POST-REFLECT-TASK.md:576: "Status set to "🔴 Blocked"; NOT flipped to Done (gate not exit-0)."
    rationale: |
      Under the source's two classes the 79 hits would have to be rewritten, which falsifies the record, so a third class is the lesser harm. The file's status is Blocked, but plan line 37 never calls the file finished, and POST-REFLECT-TASK.md:576 records the substantive work as validated with only a manual reflect gate outstanding. The necessary-deviation class stands, and the third class should still be surfaced to the user.
    recommendation: |
      In Task 1 (plan line 37) and the Constraints bullet at line 25, add one sentence: the file is a Blocked, unfinished task whose old paths are intentionally left stale, and anyone resuming it must substitute an Orca worktree. Have Task 1's inventory report this class, and its 79 of 108 hits, as the first line of the final summary. Verify with `grep -n 'Historical record' ./artifacts/worktree-hit-classification.md`.
    provenance: "Variant 1 R1-2 (base) + reviewer-1-calibration.yaml (R1-2 weak) + POST-REFLECT-TASK.md:576, Change #8"
  - id: R1-3
    headline: "Task 1 labels .gitignore as 'rewrite to Orca's default location', but Task 4 keeps the `.dev/worktrees/` entry"
    location: "plan lines 35 and 89; .gitignore:240-242"
    classification: necessary
    severity: low
    evidence: |
      Plan line 35: "`.gitignore` (2 hits, the worktree comment and the `.dev/worktrees/` entry)" under "Project worktree, rewrite to Orca's default location"
      Plan line 89: "Keep the `.dev/worktrees/` entry itself."
      .gitignore:242: ".dev/worktrees/"
    rationale: |
      Keeping the entry is a defensible safety net, but the class and action label in Task 1 would be wrong for that row, and the entry still encodes the path the source says to replace.
    recommendation: |
      Edit Task 1 (plan line 35) so the .gitignore row's action reads 'rewrite comment only; keep entry as a retired-path guard (see Task 4)'. Verify that the inventory row for .gitignore carries that action text.
    provenance: "Variant 1 R1-3 (base, unchanged)"
  - id: R1-4
    headline: "'Keep working without Orca' for the internal-checkout files is asserted only by 'file unchanged', never exercised"
    location: "plan lines 36, 135; Task 6 and Task 7 test lists"
    classification: drift
    severity: low
    evidence: |
      Plan line 135: "`git diff --stat` shows no change to `POST-REFLECT-TASK.md` or to any file classified "internal temporary checkout"."
      Plan Task 6 runs only `tests/commands/test_routing_plugin_parity.py tests/recommend/`; Task 7 runs only `tests/docs/test_tavily_doc_alignment.py`.
    rationale: |
      The source asks for internal checkouts to keep working without Orca, and the plan never runs the tests that exercise those checkouts.
    recommendation: |
      Add to Task 7: `uv run pytest tests/cli/reflect/test_isolate_reviewers_cli.py tests/troubleshoot/backtest/test_git_replay_integration.py tests/skills/test_implement_retry_revert.py -v -rs`, saved to ./artifacts/t7-internal-checkout-tests.txt. Require zero skips, or record each skip reason and repeat the run in a full-depth, non-root checkout.
      Why: test_git_replay_integration.py:56-68 skips on shallow clones; .github/workflows/test.yml:17 `actions/checkout@v4` has no `fetch-depth`; test_implement_retry_revert.py:357 skips as root. The fixtures are self-contained (test_implement_retry_revert.py:613).
    provenance: "Variant 1 R1-4 (base) + Variant 3 A-003 qualification (92%) + INV-006 + Variant 2 R2-F3 fixture citation, Change #5"
  - id: R1-5
    headline: "Task 3's new wording 'no ... link' is ambiguous against the existing upstream issue link in CLAUDE.md"
    location: "plan line 73; CLAUDE.md:251"
    classification: drift
    severity: low
    evidence: |
      CLAUDE.md:251: "> **Note**: TypeScript plugin system planned for v5.0 ([#419](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues/419))"
      Plan line 73: "no tool call or link (gh, git or Orca) that resolves to it"
    rationale: |
      The literal text of plan line 73 ("no tool call or link") covers the static URL at CLAUDE.md:251 (Variant 2 X-001 majority, 62%, contested; Variant 3 dissent: plan line 82 names only Orca `--issue`/`--pr` linking). 22 lines in 10 tracked files hold the upstream URL, including deliberate negative test fixtures (test_pre_pr_checks.py:37, :82; test_crash_recovery.py:179), so the literal reading cannot be satisfied without weakening tests.
    recommendation: |
      Narrow plan line 73 to "no tool call, and no gh or Orca link flag" and state that static references in docs and test fixtures are out of scope.
    provenance: "Variant 1 R1-5 (base) + Variant 2 X-001 majority (62%, contested) + Variant 3 R3-F6 dissent + INV-011, Change #6"
  - id: R1-6
    headline: "The fetch/pull ban is a literal reading of the source, not a deviation; only the dated Orca project-id bullet is an authorized expansion"
    location: "plan lines 73, 76"
    classification: authorized
    severity: low
    evidence: |
      MEMORY.md: "Never touch SuperClaude upstream — no push, PR, comment or Orca link to SuperClaude-Org; always --repo IronbellyOrg/IronClaude"
      source.md:1: "SuperClaude upstream is never pushed to or interacted with."
    rationale: |
      "Interacted with" (source.md:1) literally covers fetch and pull, so that ban is the faithful reading, not a deviation (Variant 2 C-005, 95%; Variant 1 conceded in Round 2). Only the dated Orca project-id bullet (plan line 76) goes beyond the source; it is an authorized expansion backed by the user's memory entry, and it is an observation, not an instruction.
    recommendation: |
      No change. Optionally mark the Orca project-id bullet 'revisit when the Orca project id changes'.
    provenance: "Variant 1 R1-6 (base) + Variant 2 C-005 (95%) + Variant 1 Round 2 concession, Change #7"
  - id: M-4
    headline: "The plan and CLAUDE.md assume an `upstream` remote that does not exist in this repository, so the Orca project-id guard may never lift"
    location: "CLAUDE.md:41; plan lines 73, 76; pyproject.toml:64-67; package.json"
    classification: drift
    severity: medium
    evidence: |
      `git remote -v` lists only `origin` (orchestrator spot-check, invariant-probe.md).
      CLAUDE.md:41: "`upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent)."
      pyproject.toml:64-67 and package.json carry SuperClaude-Org/SuperClaude_Framework URLs.
      Plan line 76: the guard holds "until `orca worktree current --json` shows the fork's id".
    rationale: |
      CLAUDE.md:41 and plan lines 73 and 76 assume an `upstream` remote. Orca's upstream project id more likely comes from the upstream URLs in pyproject.toml:64-67 and package.json, so the plan line 76 guard may never lift.
    recommendation: |
      Task 3 states the rule without depending on a remote named `upstream` (forbid any remote or URL that resolves to SuperClaude-Org/SuperClaude_Framework) and records the observed project-id source as unverified.
    provenance: "INV-001, Change #4"
  - id: M-9
    headline: "Plan line 23's confirmed Orca command list lacks `--json`, `--issue` and `--pr`, which plan lines 54, 56 and 76 use"
    location: "plan lines 23, 54, 56, 76"
    classification: drift
    severity: low
    evidence: |
      Plan line 23: "orca worktree list, orca worktree current, orca worktree rm. Do not name other Orca subcommands or flags without checking their --help first."
      Plan line 54: "Name orca worktree current --json"
      Plan line 56: "Forbid Orca GitHub link flags (--issue, --pr)"
      Plan line 76: "never pass --issue, --pr or other GitHub link flags"
    rationale: |
      The confirmed list does not include the flags the plan writes into CLAUDE.md. Mitigation: plan line 76 records `orca worktree current --json` as run.
    recommendation: |
      List those flags in the Constraint, or add a `--help` check, saving the output under ./artifacts/.
    provenance: "Variant 3 R3-F3, Change #9"
  - id: M-10
    headline: "Task 6 does not run the contract test that reads all three files Task 5 edits"
    location: "tests/skills/test_sc_recommend_routing_contract.py:27, :29, :130; plan line 116"
    classification: drift
    severity: low
    evidence: |
      tests/skills/test_sc_recommend_routing_contract.py:27: `_SKILL = _REPO / "src/superclaude/skills/sc-recommend/SKILL.md"`
      tests/skills/test_sc_recommend_routing_contract.py:29: `_COMMAND = _REPO / "src/superclaude/commands/recommend.md"`
      tests/skills/test_sc_recommend_routing_contract.py:130: `reference = (_SKILL.parent / "refs/surface-enumeration.md").read_text()`
      Plan line 116: `uv run pytest tests/commands/test_routing_plugin_parity.py tests/recommend/ -v`
    rationale: |
      Coverage gap: the test reads all three Task 5 files, and plan line 116 does not run it.
    recommendation: |
      Add tests/skills/test_sc_recommend_routing_contract.py to Task 6's pytest command.
    provenance: "Variant 3 R3-F4, Change #10"
  - id: M-11
    headline: "The post-release tag checkout offers `git worktree add` with no location and no removal, which does not match the create-and-remove exception"
    location: "src/superclaude/skills/sc-post-release-protocol/SKILL.md:91; plan line 57"
    classification: drift
    severity: low
    evidence: |
      SKILL.md:91: "read the release's code surface at that tag — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag"
      Plan line 57: "internal temporary checkouts that a CLI or test creates and removes itself"
    rationale: |
      The skill names no location and never says to remove the checkout, so it does not meet the exception as plan line 57 defines it.
    recommendation: |
      Task 2's exception text describes it as an optional read-only tag checkout removed after the scan, or Task 1 reclassifies it.
    provenance: "Variant 3 R3-F5, Change #11"
  - id: M-12a
    headline: "A live checkout still exists at the retired worktree location, and the plan does not say what happens to it"
    location: "/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates (git worktree list); Task 2"
    classification: drift
    severity: low
    evidence: |
      `git worktree list` shows /home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates (orchestrator spot-check, invariant-probe.md).
    rationale: |
      The plan says nothing about existing checkouts at the retired location.
    recommendation: |
      Task 2 says what happens to existing retired-location checkouts.
    provenance: "INV-002, Change #12"
  - id: M-12b
    headline: "docs/swarm/runbook.md:34 cites a `.claude/worktrees/BareReview` path that neither grep covers"
    location: "docs/swarm/runbook.md:34"
    classification: drift
    severity: low
    evidence: |
      docs/swarm/runbook.md:34: "- The fork's CLAUDE.md (`/config/workspace/IronClaude/.claude/worktrees/BareReview/CLAUDE.md`)"
    rationale: |
      The path is outside both greps, so no task sees it.
    recommendation: |
      Task 1 notes the runbook line or states it out of scope.
    provenance: "INV-014, Change #12"
t1_findings_disputed:
  - {t1_id: F1, reason: "Agree it goes beyond the source and covers 79 of 108 hits; classify as necessary deviation (two-class scheme would force rewriting a record); still surface to the user; the file is Blocked, not Done (R1-2)."}
  - {t1_id: F2, reason: "Mostly refuted: every file except CLAUDE.md is single-class; CLAUDE.md's 8 hits sit in one subsection replaced wholesale; Task 7 carves out retired-location or exception lines. Low severity at most."}
  - {t1_id: F3, reason: "Refuted as a deviation: fetch or pull is network interaction with upstream, so the literal reading is the faithful one; the real problem is that CLAUDE.md:64 and :66 still interact with upstream (R1-1)."}
  - {t1_id: F4, reason: "Partly disputed: 'aligned' is too strong; .gitignore:242 still encodes the path and Task 1 labels the row 'rewrite' while Task 4 keeps it (R1-3)."}
self_confidence: 0.75  # base value from reviewer-1; not recomputed by the merge
coverage:
  provenance: "Variant 2 structure (S-001 winner), Change #13"
  source: "artifacts/pass2-inferred.yaml"
  inferred_requirements_total: 11
  missing_in_plan_substance:
    - id: INF-003
      status: partial
      note: "'every tracked file' is not fully covered; list-argument worktree creations escape the spec grep"
      carried_by: [M-1, M-2]
  requirements:
    - {id: INF-001, status: covered}
    - {id: INF-002, status: covered}
    - {id: INF-003, status: partial, carried_by: [M-1, M-2]}
    - {id: INF-004, status: covered}
    - {id: INF-005, status: covered}
    - {id: INF-006, status: covered}
    - {id: INF-007, status: covered}
    - {id: INF-008, status: covered}
    - {id: INF-009, status: covered}
    - {id: INF-010, status: covered}
    - {id: INF-011, status: covered}
invariants_carried:
  - {id: INV-001, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding M-4"}
  - {id: INV-002, severity: LOW, status: "UNADDRESSED in plan; carried by finding M-12a"}
  - {id: INV-003, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding M-2"}
  - {id: INV-004, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding M-2"}
  - {id: INV-005, severity: HIGH, status: "UNADDRESSED in plan, convergence-blocking; carried by finding M-1"}
  - {id: INV-006, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding R1-4 (zero-skip rule)"}
  - {id: INV-008, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding R1-1 (recovery gap)"}
  - {id: INV-009, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding R1-1 (gh-flag gap)"}
  - {id: INV-010, severity: MEDIUM, status: "UNADDRESSED in plan; no finding, carried as an inferred claim (Change #14)"}
  - {id: INV-011, severity: MEDIUM, status: "UNADDRESSED in plan; carried by finding R1-5"}
  - {id: INV-014, severity: LOW, status: "UNADDRESSED in plan; carried by finding M-12b"}
changes_not_made:
  - diff_point: C-001
    non_base_approach: "Variant 3 fix of check 1 with `gh repo set-default --view` only"
    rationale: "Leaves CLAUDE.md:66; Variants 2 and 3 conceded (97%)"
  - diff_point: "U-006 / R2-F4"
    non_base_approach: "Rewrite the `.claude/` staging constraint"
    rationale: "Withdrawn by its advocate; misquotes .gitignore:129; plan copies CLAUDE.md's absolute rule. Recorded as informational: `.claude/cache/sc-recommend-lookup.yaml` is tracked"
  - diff_point: S-002
    non_base_approach: "Variant 3 all-drift labels"
    rationale: "Conceded by Variant 3"
  - diff_point: "Variant 2 missing_requirements: []"
    non_base_approach: "Empty missing list"
    rationale: "Disproved by scripts/eval_runner.py:143"
  - diff_point: "U-007 as a finding"
    non_base_approach: "Raise sc-pr-submit SKILL.md:267 as drift"
    rationale: "Round 2 showed the fallback is guarded; kept informational"
inferred_claims:
  - "[INFERRED] Could not run git grep; a ripgrep count excluding .dev/.git/.claude matched 108 hits in 17 files with the plan's per-file counts."
  - "[INFERRED] Did not verify `orca worktree rm` selector syntax or commit 08b1a5f8."
  - "[INFERRED] Assumes make sync-dev does not write plugins/superclaude/, so the manual byte-copy in Task 6 is required."
  - "[SUPERSEDED by the U-007 guard verdict, Round 2] [INFERRED] src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:267 uses `gh repo view --json nameWithOwner` as a fallback; in tension with the new rule but out of the hit set; not raised as a finding."
  - "[INFERRED] INV-010: bare gh calls in sc-auggie-review-protocol/SKILL.md:30, :97, :127, :319, :331 and sc-troubleshoot-protocol/SKILL.md:207; whether gh resolves them to the upstream parent when only `origin` exists is inferred, not verified. (Change #14)"
  - "[INFORMATIONAL] U-007: the sc-pr-submit SKILL.md:267 fallback is guarded (runs only if origin has no URL; same guard in the pr-submit scripts); not raised as a finding. (Change #14)"
```
