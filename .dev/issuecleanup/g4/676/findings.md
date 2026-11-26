## Verdict
**still-relevant**. Issue [#676](https://github.com/IronbellyOrg/IronClaude/issues/676), the report about forced installer overwrites without recovery copies, remains OPEN with no comments at the live read on 2026-11-24. This is not yet an accepted requirement to add backups: the issue explicitly permits a documented policy instead and asks for the owner's decision before changing behavior.

At checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, all three reported overwrite paths still exist:
- Core files: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_core.py:68-79` skips existing files only without force, then copies directly without saving the target.
- Agents: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_agents.py:47-59` has the same direct-copy behavior.
- Templates: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_templates.py:70-79` also directly replaces existing targets under force.
- The entry points expose all three: install forwards its force argument at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/main.py:180`, `:198`, `:229`; update always passes true at `:383`, `:396`, `:417`. A successful copy can therefore discard local edits without these functions creating a recovery copy.

Partial resolution exists in documentation, not in those overwrite paths. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/installation.md:613` and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/upgrading.md:38-56` already warn that core files, agents and skills have no saved copy, but omit templates. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_keep.py:1-7` still promises saved copies before forced overwrites without limiting that promise to installers which call it. The issue's documentation-only acceptance route is therefore unfinished too.

Merged PR #480 (`5fa680778718af9087ccbe7a823e3909f1bcceb6`) deliberately added backups only to commands and user setup and expressly excluded core, agents and templates. PR #646 (`ffb37863054a02adc6ef7172623c6d28bc7d52f8`) fixed cached content comparison, not backup adoption. PR #673 (`b68d5eeaf618a8e33cde55cb660acfdd8f321f67`) recorded this as an out-of-scope follow-up, not a completed fix. Live PR search for `676`, backup-related titles/bodies and open `install` PRs found no implementing PR; this is bounded search evidence, not proof that no unmentioned branch exists.

Required command completed: `/sc:analyze src/superclaude/cli --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/676/analyze`. This is the narrowest common source directory for the relevant files, with analysis limited to installer architecture. Evidence report: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/676/analyze/analyze-report.md`.

UNVERIFIED: actual user-data loss, runtime reproduction, platform-specific copy failures, and any owner decision outside the live issue and reviewed PRs. No installer or tests were executed, no UV or package operation was run, and no source or GitHub state was changed.

## Complexity and size
**complexity medium; size S.** The behavior-changing route spans three installers, backup-failure handling and regression checks but can reuse the existing helper; the explicitly allowed documentation-only route is smaller (simple, XS), pending the owner's policy choice.

## Priority
**P2.** Updates can discard edits to important instruction files, but existing guide warnings already cover core files and agents, the issue is a policy lead rather than an agreed backup requirement, and no release or dependent issue is verified blocked; resolve the remaining policy and documentation gap before another installer behavior change.

## Concrete next steps
1. Coordinator obtains and records the owner's choice for each of core files, agents and templates. Keep this issue open until that choice and its matching implementation or documentation are complete; do not treat this review as permission to change overwrite behavior.
2. Smallest accepted route: retain current copying behavior, narrow `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_keep.py:1-7` to the actual protected installer types, and explicitly name templates alongside core files and agents in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/installation.md:613` and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/upgrading.md:43-47`. Record the no-backup decision for each type.
3. Only if backups are chosen for a type: reuse `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_keep.py:40-50` before replacing its existing target. Follow the command installer's failure guard at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_commands.py:65-79`: on failed backup, report failure and leave the target untouched, rather than catching the error and continuing to overwrite.
4. For any behavior-changing route, extend the existing patterns in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_keep.py:121-193` to the affected core, agent and template installers: edited file saved before replacement, unchanged file not backed up, non-force preservation, backup failure leaves original bytes intact and reports failure. Verify both install and update entry-point behavior in the existing CLI tests. A new helper or wholesale installer rewrite is unnecessary.

## Dependencies
No issue-number prerequisite or issue blocked by #676 was established from the issue, its comments, the reviewed PRs or the bounded related-issue searches. The owner policy choice is a decision dependency, not a verified numbered issue. #606 is provenance only, not a prerequisite.

## Related issues
- [#606](https://github.com/IronbellyOrg/IronClaude/issues/606), closed observer visual-parity work: its branch and PR #673 surfaced this installer follow-up; it does not solve or block #676.
- [#346](https://github.com/IronbellyOrg/IronClaude/issues/346), review-loop work: the historical source of the limited backup change in PR #480, as explicitly stated in that PR. Its live issue body and current state were not needed for this installer verdict and remain UNVERIFIED here; no dependency is inferred.
- No separate duplicate found by `gh issue list` searches for `installer backup` and `"backup" in:title`. PR #419 is a pull request, not an additional issue, despite its number appearing in the historical discussion.

## Related PRs
- [#673](https://github.com/IronbellyOrg/IronClaude/pull/673), merged observer visual parity, commit `b68d5eeaf618a8e33cde55cb660acfdd8f321f67`: directly mentioned by the issue's branch context, read with its live discussion; its body explicitly leaves the no-backup behavior as a follow-up.
- [#646](https://github.com/IronbellyOrg/IronClaude/pull/646), merged stale content-comparison fix, commit `ffb37863054a02adc6ef7172623c6d28bc7d52f8`: makes the shared comparison accurate and routes core comparisons through it; adds no forced backup to the three reported installers.
- [#480](https://github.com/IronbellyOrg/IronClaude/pull/480), merged kept-file warnings and forced backups, commit `5fa680778718af9087ccbe7a823e3909f1bcceb6`: introduced the existing helper and applied it to commands and user setup; explicitly excludes core, agents and templates.
- [#419](https://github.com/IronbellyOrg/IronClaude/pull/419), merged kept-core warning, commit `d8229171042490d6e16436abbca392cee73e0e06`: reports differing files when kept; does not preserve edited files under force.
- [#497](https://github.com/IronbellyOrg/IronClaude/pull/497), closed without merge integration proposal mentioning #480 and #606: not a fixing PR; its body was returned by the provenance search and is not treated as completed work.
