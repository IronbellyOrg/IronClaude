# Issue 553 review

Template: findings structure from /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/550/report-template.md, mapped to the brief's required fields.

## Verdict and evidence
**still-relevant.** Keep [issue #553, default installation of the TypeSafe Jev skill](https://github.com/IronbellyOrg/IronClaude/issues/553) open: this checkout has neither the default plugin nor its catalog entry. The complete defaults contain seven enabled plugins and one pinned catalog entry, Ponytail, with no TypeSafe entry (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/user_settings_defaults.json:29-69).

The issue's older NEEDS-OWNER-DECISION comment is superseded: the [owner's 2026-11-17 comment](https://github.com/IronbellyOrg/IronClaude/issues/553#issuecomment-6941538923) selects installation pinned to a tag. Selecting and reviewing the actual tag remains unfinished, not the pinned-versus-unpinned decision.

Snapshot: local HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on 2026-11-24. The issue is OPEN and its closure-linked PR list is empty. Searches for `553` and `typesafe` across all PR states returned no matches. Existing installation machinery predates the request: PR #360 (`c83e3d78da4367bd44f61f65d1490fb3dd7119af`) and PR #369 (`7632090d7389977dc0648054ccff34ddb972421d`) implement and harden Ponytail pinning, not TypeSafe installation.
## Real current state
Nothing of the issue is implemented in this checkout:
- No TypeSafe plugin in the defaults. `enabledPlugins` has seven entries, none TypeSafe; `ironclaudeMarketplace.plugins` has one entry, Ponytail (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/user_settings_defaults.json:29-69).
- No installer code change needed or made for the plugin: `install_plugins` already handles any catalog entry generically, deriving the pin map from the catalog and installing or updating at the pinned commit (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_user_setup.py:362-406, 411-455).
- No TypeSafe or Jev references anywhere under `src/` or in the installer tests (case-insensitive Grep, zero matches). The docs mentions of Jev/TypeSafe live in `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md`, an operational guide for the gateway route, not plugin installation; it confirms nothing in `src/` calls Jev and that the client exists only in an experiment tree.
- No open or merged PR mentions 553, `typesafe` or `Jev` as installation work; the closest, PR #500, merged experiment artifacts on 2026-11-11 with no installer changes.
## Concrete next steps
1. Resolve the actual release tag and its full 40-character commit from the TypeSafe skills repository, and review the skill text at that commit before pinning it. The issue's own recommendation is to pin only when a release tag exists; whether one exists is still "Not known yet" and was not checked here.
2. Add the TypeSafe entry to `ironclaudeMarketplace.plugins` and `enabledPlugins` in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/user_settings_defaults.json, with `ref`, `sha` and a description ending `pinned by IronClaude`, following the Ponytail entry at lines 59-69.
3. Extend /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_user_setup.py so the new entry's source, the 40-character shape check and the default-plugin map assertion cover TypeSafe, mirroring the Ponytail tests at lines 113-137.
4. Document the new default in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/installation.md, including that each user supplies their own key and that the installer sends no data by default, following the Ponytail section at lines 383-411.
5. After merge, verify that Coder's Renovate proposes a pin-update PR for a new TypeSafe release tag, as required by the selected pinned route; a source listing alone is not success. Open a Coder follow-up only if that pinned-route check fails (issue #553, Proposed Solution step 3 and the owner's 2026-11-17 decision). Result: UNVERIFIED until the tag/pin-update proposal is observed; Coder was not accessed here.
## Complexity and size
**simple, S.** The installer already handles any catalog entry generically (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_user_setup.py:362-406), so the change is one defaults entry, matching tests and a docs note. The only non-mechanical part is choosing and reviewing the tag and commit.
## Priority
**P2.** It unblocks nothing in this repository: no source under `src/` calls Jev, and the blocker-classifier work (issue #552) gives the classifier no authority in version 1 and requires a separate owner decision and an API key before any real Jev run. The impact is convenience for future typed-decision steps, not a current blocker.
## Dependencies
- Needs: a release tag and commit from the TypeSafe skills repository, and a review of the skill text at that commit. Both are outside this repository and not done.
- Blocks: nothing verified. Issue #552 (blocker classification) mentions Jev as a candidate engine but its own comment says the classifier has no authority in version 1 and a real Jev run needs a separate owner decision plus an API key, so #553 does not gate it.
- Blocked by: nothing in this repository.
## Related issues
- [Issue #552, blocker classification](https://github.com/IronbellyOrg/IronClaude/issues/552), OPEN: named Jev as a candidate; its 2026-11-17 comment says the classifier has no authority in version 1 and a real Jev run needs an owner decision and an API key.
- [Issue #463, Jev router research](https://github.com/IronbellyOrg/IronClaude/issues/463), CLOSED 2026-11-17 as not needed now; no research completed.
- Issues #609, #610, #611 and #612 (Jev preflight steps), OPEN: separate Jev evaluation work, not plugin installation. Titles verified by `gh issue list`; bodies not read.
- [Issue #574, fast-jev compaction](https://github.com/IronbellyOrg/IronClaude/issues/574) and [issue #575, jev-pruner](https://github.com/IronbellyOrg/IronClaude/issues/575), both CLOSED on hold with no live testing. Titles verified; bodies not read.
- Coder #419 (central upstream monitor) and Coder #478 (BMAD and Ponytail defaults), named in the issue body: not read here, since the brief restricts GitHub reads to IronbellyOrg/IronClaude.
## Related PRs
- None implement #553. Searches for `553` and `typesafe` across all PR states returned no matches, and the issue's closure-linked PR list is empty.
- Precedent only: [PR #358](https://github.com/IronbellyOrg/IronClaude/pull/358) (merged 2026-11-04, `9b9497e64b830f735aac2765ebb74ed658d183f1`) first installed Ponytail unpinned; [PR #360](https://github.com/IronbellyOrg/IronClaude/pull/360) (merged 2026-11-04, `c83e3d78da4367bd44f61f65d1490fb3dd7119af`) moved it to the pinned `ironclaude` catalog; [PR #369](https://github.com/IronbellyOrg/IronClaude/pull/369) (merged 2026-11-04, `7632090d7389977dc0648054ccff34ddb972421d`) hardened the pin checks. These are the pattern #553 should follow, not work on #553.
## Verification limits and negative evidence
- UNVERIFIED: whether the TypeSafe skills repository publishes a release tag, and its latest tag and commit. No network fetch of that repository was made; the issue itself records this as "Not known yet".
- UNVERIFIED: the Coder repository's upstream monitor state and whether it would watch the new source automatically. Its config lives in IronbellyOrg/PrivateRepoF, which the brief puts out of scope.
- UNVERIFIED: bodies of issues #609, #610, #611, #612, #574 and #575. Only their numbers, titles and states were read.
- Negative evidence: case-insensitive Grep for TypeSafe, `TYPESAFE_API_KEY` and Jev under `src/` and in `tests/cli/test_install_user_setup.py` returned zero matches; `gh pr list --search '553'` and `--search 'typesafe'` returned empty lists; the issue's closure-linked PR list is empty.
- No tests or installs were run; all code claims are from static reads of the files cited above.
