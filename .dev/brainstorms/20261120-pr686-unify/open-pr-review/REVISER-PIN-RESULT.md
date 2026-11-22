# Reviser pin fix: result

- Base: origin/master f2904292eed1f6710ebc5dca2eb48394fd1775f6 (contains merged PR 696; refs/remediation.md present)
- Branch: ironbelly/issue-624-pin-reviser (new, pushed normally, no force)
- Commit: c467d53be9efd99a4ad857796d8cb47753ddec93 (one commit)
- Remote check: `git ls-remote --heads origin ironbelly/issue-624-pin-reviser` printed c467d53be9efd99a4ad857796d8cb47753ddec93
- Checkout used: /home/coder/workspaces/worktrees/IronClaude/reviser-pin-fix (existing worktree; no other worktree created)

## Files (7, 81 insertions, 5 deletions)
- docs/user-guide/agents.md
- plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
- plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md
- src/superclaude/skills/sc-workflow-protocol/SKILL.md
- src/superclaude/skills/sc-workflow-protocol/refs/remediation.md
- src/superclaude/agents/workflow-reviser.md (new)
- tests/agents/test_workflow_reviser_readonly.py (new)

## Differences from the issue-624 worktree copy
None. The five diffs (vs origin/ironbelly/issue-624 = 6ba2b5117) applied cleanly with `git apply --3way`; the two new files were copied; `cmp` of all seven files against the other worktree reported identical. That worktree was only read.

## Tests
- tests/agents/test_workflow_reviser_readonly.py: 3 passed
- make sync-dev, make verify-sync: "All components in sync"
- make lint: all checks passed
- Full `uv run pytest -q`: 2 failed, 23520 passed, 44 skipped (1405 s)
  - FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
  - FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
  - Both are pre-existing/environmental: they run `.venv/bin/python -m ruff`, and the venv has no ruff module ("No module named ruff"). The same two fail the same way on a clean `git archive origin/master` export in /tmp/pinfix-master. The first passes there with `uv run --with ruff`.
- Nothing under .claude/ staged.

## Deviations
- The sc-workflow-protocol and agent/plugin sync tests were covered by the full suite, not run separately.
- Nothing else on GitHub touched: no PR, comment, label or merge.

## Status: PR opened (2026-11-20, 17:45 UTC)
- PR 705: https://github.com/IronbellyOrg/IronClaude/pull/705 (opened with `/sc:pr-submit --monitor 3`, `--repo IronbellyOrg/IronClaude`; URL checked). Base master f2904292e, head c467d53be, 1 ahead / 0 behind, mergeable, no conflicts.
- Not to be merged until the owner says so.

## Status: round 1 (review at 17:49 UTC)
- Codex: clean (no findings).
- Augment: 2 Medium findings, both verified by a read-only evidence-validator agent and both about code this PR adds:
  1. `refs/remediation.md` line 63 (plugin mirror too): "project copy second" was wrong, Claude Code reads the project agent first, so a repo could shadow `workflow-reviser` with broader tools. Fixed: the coordinator must Read both definitions that exist and stop unless each has exactly `Read, Edit, Grep, Glob`.
  2. `workflow-reviser.md` line 5: Edit cannot be path-scoped. Fixed: the coordinator records and re-checks sha256 of the original plan and review report plus `git status --porcelain` around the reviser; any change outside the copy dir means release and escalate.
- Fix commit 5f603c707 (second commit on the branch), pushed fast-forward (c467d53be..5f603c707). Checks: new test file 4 tests, tests/agents + tests/skills 2351 passed, make lint and make verify-sync clean. `ruff format --check src/ tests/` reports 6 files (for example src/superclaude/examples/release-spec-template.md); none are files this PR touches (the test file I edited is clean).
- Both threads replied to and resolved. Re-review requested from Augment ("augment review") and Codex ("@codex review") at 17:54:57 / 17:55:00 UTC; waiting for results.

## Status: round 2 (review at 17:57 UTC)
- Augment: 1 Medium. The `git status --porcelain` check misses ignored files, paths outside the root and content changes to an already-modified file. Verified; code added by this PR.
- Codex: 1 Medium (P2). The plugin copy of the protocol requires `workflow-reviser` but the agent was not in `plugins/superclaude/agents/`, so a plugin-only install would always stop. Verified (the plugin build copies agents only from `plugins/superclaude/agents/`); code added by this PR.
- Fix commit e00ac26fe (third commit), pushed fast-forward (5f603c707..e00ac26fe). Content digest (`ls-files` plus `sha256sum`) replaces the git status check, with its remaining blind spots named in the text; byte copy of the agent added under plugins/superclaude/agents/ plus a plugin-suffix sentence and a byte-parity test. Checks: tests/agents + tests/skills + tests/unit/test_cli_install.py 2446 passed, make lint and make verify-sync clean.
- Both threads replied to and resolved. Re-review requested from both reviewers at 18:02:56 / 18:02:59 UTC. This is the last fix round under the default cap of 2 rounds; findings after it are reported, not fixed.
- Known, not changed: `reflect-reviewer` (used by section 4 of remediation.md and not added by this PR) also has no plugin copy. Pre-existing gap, left for a follow-up.

## Status: round 3 and final (2026-11-20, 18:11 UTC): halted at the round cap
- Head e00ac26fe. Codex: clean. Augment: 1 Medium (thread PRRT_kwDOPOT5c866HIXe, `refs/remediation.md` line 64, plugin copy too): `git ls-files` lists the tracked submodule folder `.vendor/anthropic-skills`, which `sha256sum` cannot hash, so edits inside it are missing from the checkout digest. NOT verified by the evidence-validator (the cap stops further fixes) and NOT fixed; thread left open, no reply. Proposed fix if a third round is allowed: skip submodule entries (for example `git ls-files -z --stage` filtered to non-160000 modes) in the digest.
- Run ended `terminal_max_rounds`: 2 fix rounds used (the default `--max-rounds 2`), 2 fix pushes (5f603c707, e00ac26fe), 3 commits on the branch.
- CI on e00ac26fe: clean. All 6 checks passed (Test Summary, SuperClaude Doctor Check, Test on Python 3.10, Lint, Plugin, Sync and Dependency Checks, Swarm imm lane, Swarm inv lane). Mergeable: CLEAN.
- PR 705 is not merged and must not be merged until the owner says so. No force push at any point.
- Follow-ups not done: `reflect-reviewer` has no plugin copy (older gap); the submodule finding above.

## Status: round 3 (owner allowed one more round, 2026-11-20 18:23 UTC) and final
- Open finding of the previous status (submodule folder in the digest): reproduced here ("sha256sum: .vendor/anthropic-skills: Is a directory"), fixed in commit da48e1001 (fourth commit), pushed fast-forward (e00ac26fe..da48e1001). Digest drops that error and adds `git submodule foreach` hashing; remaining blind spots named in the text. tests/agents + tests/skills 2352 passed, lint and verify-sync clean. Thread replied to and resolved. Verified by reproduction, not by the evidence-validator agent.
- Re-review of da48e1001: Codex clean. Augment: 1 finding labelled High (thread PRRT_kwDOPOT5c866HwyM, `refs/remediation.md` line 64, plugin copy too): the digest hashes the whole checkout including "the permitted copy directory", so a legitimate copy edit and an out-of-copy edit cannot be told apart. NOT fixed, thread left open, no reply (the extra round is used).
  - My reading: the claim rests on a wrong premise. `prepare` puts the copy in `/tmp/sc-workflow-revise.XXXXXXXX/<new-id>/` (remediation.md line 45), outside `<root>`, so the checkout digest never includes the copy and ANY difference is an out-of-copy edit. The leaf `.dev/tasks/to-do/<new-id>/` is created by `reserve` before the digest is taken. The real defect is wording: "Any difference, other than the copy directory" suggests the copy is inside the digest. Proposed fix: say "any difference at all (the copy is under /tmp, outside <root>)". Not verified by an independent agent.
- CI on da48e1001: clean, all 6 checks passed; mergeable CLEAN.
- PR 705 not merged; no force push; 4 commits on the branch (c467d53be, 5f603c707, e00ac26fe, da48e1001).

## Status: independent check of the open Augment finding (2026-11-20, 20:24 UTC)
- A separate read-only evidence-validator agent was given the finding and the files, not my reading. Verdict: UNVERIFIED (the central claim is false), confirming my reading.
  - The copy is in `/tmp/sc-workflow-revise.XXXXXXXX/<new-id>/` (remediation.md line 45), outside `<root>`; the digest covers only `<root>` (line 63), so a copy edit cannot mask an in-root edit.
  - The one in-root place the reviser may touch, the leaf `reserve` creates, is empty between the before and after digests, and a file written there would change the digest (correctly).
  - Real defect: wording only. "Any difference, other than the copy directory" wrongly suggests the copy is hashed. Suggested text: "Any difference means it edited something else."
  - No new security gap. The gaps the text already names (ignored files, untracked files in submodules, paths outside `<root>`) stay, with the `tools:` allowlist as the main control.
  - The finding's line number is off by one: the digest text is on line 63, not 64 (the agent read only the src/ file).
- Thread PRRT_kwDOPOT5c866HwyM is still open, with no reply. Nothing changed on the branch (still da48e1001). PR 705 is not merged.

## Status: merged (2026-11-20, 20:27 UTC, on the owner's chat go "yes post and then merge")
- Replied on thread PRRT_kwDOPOT5c866HwyM (comment 4646256551) explaining the misreading (copy is in /tmp, outside the digest); left unresolved, no code change.
- Merge checked first: PR OPEN, not draft, MERGEABLE, CLEAN, head da48e1001, all 6 checks passed, 0 behind master.
- Squash-merged with `gh pr merge 705 --repo IronbellyOrg/IronClaude --squash --match-head-commit da48e1001...`. Merge commit on master: 1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9 ("... (#705)").
- Not done: the branch `ironbelly/issue-624-pin-reviser` was not deleted; the open Augment thread was not resolved; `reflect-reviewer` still has no plugin copy.

- Remote branch ironbelly/issue-624-pin-reviser deleted on the owner's chat "yes" (20:28 UTC); local branch and worktree kept.
