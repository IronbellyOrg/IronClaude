# Returned by reflect-reviewer (read-only); persisted verbatim by the orchestrator.
reviewer: 3
persona: refactorer
model_class: opus
findings:
  - id: R3-F1
    headline: The hit search misses a script that runs `git worktree add` as a list of arguments, so the new CLAUDE.md rule will forbid a script the plan never classifies
    location: scripts/eval_runner.py:143
    classification: drift
    severity: medium
    evidence: >-
      scripts/eval_runner.py:138 `worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"`;
      scripts/eval_runner.py:143 `["git", "worktree", "add", str(worktree_path), "master"],`;
      plan TASK-WF-...md:19 `The hit set is the output of git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'`;
      plan :57 `internal temporary checkouts that a CLI or test creates and removes itself keep using git worktree add directly ... Name the four cases from Task 1`
    rationale: >-
      The script splits "worktree" and "add" into separate list items, so the regex at plan :19 cannot match them. The worktree it creates outside Orca is persistent and the script never removes it, so it fits none of the four named exceptions. The Goal (plan :15) and requirement INF-003 ("every tracked file") are left with a tracked tool that the new absolute rule forbids.
    recommendation: >-
      In Task 1 (plan :33), add a second search,
      `git grep -n -E '"worktree",\s*"add"|worktree", "add' -- ':!.dev'`, and add
      scripts/eval_runner.py to the inventory with a class and a reason (likely a fifth internal-checkout case or a
      project-worktree rewrite). In Task 2 (plan :57), either name it as an exception or say the exception list is
      illustrative. Verify by checking that the Task 7 residual check covers this second search too.
  - id: R3-F2
    headline: Task 3's ban on any call that reaches upstream contradicts pre-PR check 1, which the plan keeps
    location: CLAUDE.md:64
    classification: drift
    severity: medium
    evidence: >-
      CLAUDE.md:64 `Then gh repo view --json nameWithOwner -q .nameWithOwner must print IronbellyOrg/IronClaude; if it prints the upstream parent, run gh repo set-default ...`;
      plan :73 `no tool call or link (gh, git or Orca) that resolves to it`;
      plan :78 `the pre-PR checks ... stay. Edit them only where they contradict the rules above.`
    rationale: >-
      Check 1 deliberately runs a gh call that queries the upstream repo when the default is wrong. That is exactly the "tool call that resolves to it" the new rule bans. The plan names neither this conflict nor a fix, so the executor must decide alone, and an acceptance check at plan :82 could pass with the contradiction still in place.
    recommendation: >-
      In Task 3 (plan :78), name check 1 explicitly. Replace it with a check that makes no network call: run
      `gh repo set-default IronbellyOrg/IronClaude` first, then confirm with `gh repo set-default --view` (check
      `gh repo set-default --help` before writing it). Add an acceptance line to plan :82: the section contains no
      `gh repo view` without an explicit `IronbellyOrg/IronClaude` argument.
  - id: R3-F3
    headline: The plan names Orca flags that its own list of confirmed commands does not include
    location: .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md:23
    classification: drift
    severity: low
    evidence: >-
      plan :23 `orca worktree list, orca worktree current, orca worktree rm. Do not name other Orca subcommands or flags without checking their --help first.`;
      plan :54 `Name orca worktree current --json`;
      plan :56 `Forbid Orca GitHub link flags (--issue, --pr)`;
      plan :76 `never pass --issue, --pr or other GitHub link flags`
    rationale: >-
      The confirmed list has no `--json`, `--issue` or `--pr`, yet Tasks 2 and 3 write them into CLAUDE.md with no `--help` check. Only `orca worktree rm` gets one (plan :58).
    recommendation: >-
      Either add `--json` (from `orca worktree current --help`) and `--issue`/`--pr` (from `orca worktree create --help`)
      to the confirmed list at plan :23, or add a `--help` check step to Tasks 2 and 3 matching the one at plan :58.
      Verify that each Orca flag in the final CLAUDE.md appears in a `--help` output saved under ./artifacts/.
  - id: R3-F4
    headline: Task 6 skips the test that pins the text of the files it edits
    location: tests/skills/test_sc_recommend_routing_contract.py:27
    classification: drift
    severity: low
    evidence: >-
      tests/skills/test_sc_recommend_routing_contract.py:27 `_SKILL = _REPO / "src/superclaude/skills/sc-recommend/SKILL.md"`;
      :29 `_COMMAND = _REPO / "src/superclaude/commands/recommend.md"`;
      :130 `reference = (_SKILL.parent / "refs/surface-enumeration.md").read_text()`;
      plan :116 `run uv run pytest tests/commands/test_routing_plugin_parity.py tests/recommend/ -v`
    rationale: >-
      This test reads all three files Task 5 edits, and the plan never runs it. The strings it currently pins do not overlap the planned edits, so it will most likely pass, but it is the right safety check for these files.
    recommendation: >-
      At plan :116, add `tests/skills/test_sc_recommend_routing_contract.py` to the pytest command and keep saving
      the output to ./artifacts/t6-pytest.txt.
  - id: R3-F5
    headline: The release-tag checkout is classified as an internal temporary checkout, but its text sets no location and no removal
    location: src/superclaude/skills/sc-post-release-protocol/SKILL.md:91
    classification: drift
    severity: low
    evidence: >-
      SKILL.md:91 `read the release's code surface at that tag — e.g. git show <tag>:<path>, git ls-tree <tag>, or a git worktree add / git archive checkout of the tag`;
      plan :57 `internal temporary checkouts that a CLI or test creates and removes itself`
    rationale: >-
      The skill offers `git worktree add` only as one option. It names no location and never says to remove the checkout, so it does not meet the exception's definition. Run in this repo, it could leave an untracked worktree that the new rule forbids.
    recommendation: >-
      In the Task 1 inventory reason and the Task 2 exception text, describe this case as "an optional read-only tag
      checkout, removed after the scan". If that does not hold, either reclassify the line or note it as an
      accepted edge case. Verify that the row's reason in ./artifacts/worktree-hit-classification.md matches the
      wording at SKILL.md:91.
  - id: R3-F6
    headline: CLAUDE.md keeps a link to an upstream issue that Task 3's wording may forbid
    location: CLAUDE.md:251
    classification: drift
    severity: low
    evidence: >-
      CLAUDE.md:251 `> **Note**: TypeScript plugin system planned for v5.0 ([#419](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues/419))`;
      plan :73 `no tool call or link (gh, git or Orca) that resolves to it`
    rationale: >-
      The tightened rule bans links that resolve to upstream, but the same file still invites a reader to open an upstream issue. Task 3 is limited to the PR section, so this line is never reviewed.
    recommendation: >-
      Either add a bullet to Task 3 to unlink or remove the reference at CLAUDE.md:251, or narrow plan :73 to say
      "link flags" so it clearly covers only Orca and gh arguments. Verify with
      `grep -n 'SuperClaude-Org/SuperClaude_Framework' CLAUDE.md`: every remaining hit should state the prohibition.
t1_findings_disputed:
  - t1_id: S4
    reason: >-
      The Orca surface is only partly limited to verified help output. Plan :23 confirms only create, list, current
      and rm, yet plan :54, :56 and :76 name `--json`, `--issue` and `--pr` with no `--help` check. Only
      `orca worktree rm` has one (plan :58). See R3-F3.
  - t1_id: S1
    reason: >-
      Partly disputed. The mirror order and parity test are correct, but Task 6's tests skip the direct contract test
      for the edited files, tests/skills/test_sc_recommend_routing_contract.py:27-30,130 (see R3-F4).
self_confidence: 0.8
inferred_claims:
  - "[INFERRED] `git check-ignore -q .dev/worktrees/example` exits 0 even though the path does not exist, because git treats a match on the parent directory pattern `.dev/worktrees/` (.gitignore:242) as excluding the path. Not run (no shell access)."
  - "[INFERRED] `gh repo set-default --view` prints the configured default repository locally without an API call to the target repo. Not checked against `gh --help` here."
  - "[INFERRED] `--json` on `orca worktree current` and `--issue`/`--pr` on `orca worktree create` exist. Could not check Orca `--help` output."
  - "[INFERRED] Orca reports the project id as `github:superclaude-org/superclaude_framework` because of the `upstream` remote or the upstream URLs in pyproject.toml:64-67. Not verifiable read-only."
  - "[INFERRED] The editable install's force-included copies (.venv/.../superclaude/_src and _plugins, used by tests/unit/test_cli_install.py:480-493) may hold old copies of the sc-recommend files until a reinstall. Not judged."
