# Default plugin installation architecture analysis

Template: analyze structure from /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/550/report-template.md, with scope set by the analyze command.

## Scope and grounding
- Command: `/sc:analyze src/superclaude/cli/install_user_setup.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/553/analyze`.
- Scope: the plugin installation entry point and its adjacent defaults, installer tests and installation documentation. Static reads only; no installs, API calls, builds or tests.
- Local HEAD: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, inspected on 2026-11-24. Remote source freshness was not checked.
- Codegraph: index_state=fresh, checked_at=2026-11-24T02:49:11Z; degraded: none. Source reads, not graph rows, establish the findings.
## Architecture and metrics
The existing architecture already supports another pinned plugin without a new installer subsystem:
1. Defaults are loaded from adjacent JSON and merged without overwriting existing settings; the private catalog is excluded from settings (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_user_setup.py:204-244).
2. The installer derives wanted plugins from enabled defaults and builds its pinned-plugin map from catalog entries, including the marketplace name and full commit SHA (same file:375-406).
3. It writes the local catalog, refuses a same-named marketplace from another source, registers or refreshes its own marketplace, then installs missing plugins and updates stale pins (same file:411-455).
4. Calls are bounded by a shared time budget; marketplace failures suppress dependent installs and warnings name unfinished items (same file:459-495). The user-setup entry point calls settings application before plugin installation (same file:498-508).

Metrics: the defaults contain 7 enabled plugins, 2 external marketplace registrations and 1 pinned catalog entry, which is Ponytail, not TypeSafe (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/user_settings_defaults.json:29-69). These are static configuration counts, not runtime success rates.
## Severity-rated findings
- Medium: a new pinned catalog entry is not a data-only change end to end. A review of the source at the pin is expected before the tag is accepted, and the installer tests assert the exact catalog source, so the expected test additions include the TypeSafe entry, the resolved tag and its commit, and the updated default plugin map (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_user_setup.py:113-137). Without these, the pin is invisible to the defaults and the plugin is not installed.
- Note: the installer loads defaults at process start, so a changed catalog takes effect on the next `superclaude install` run; no additional wiring is needed beyond the defaults, tests and docs.
- Note: `install_plugins` reads only user-scope plugin records (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_user_setup.py:386-393), so the new entry behaves the same as Ponytail: a project-scope copy does not prevent a user-scope install.
## Recommendations and roadmap
- Add the TypeSafe entry to the pinned catalog and `enabledPlugins` in the defaults, with the tag, full 40-character commit and a description ending `pinned by IronClaude`, following the Ponytail entry (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/user_settings_defaults.json:59-69).
- Extend `tests/cli/test_install_user_setup.py` with the entry's source, the 40-character shape check and a TypeSafe-aware default-plugin map assertion, mirroring the Ponytail tests at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_user_setup.py:113-137.
- Document the new default and the no-API-key rule in `docs/getting-started/installation.md`, following the Ponytail section at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/getting-started/installation.md:383-411.
- Post-merge, verify that Coder's Renovate proposes a pin-update PR for a new TypeSafe release tag, as required by the selected pinned route; a source listing alone is not success. Open a Coder follow-up only if that pinned-route check fails (issue #553, Proposed Solution step 3 and the owner's 2026-11-17 decision). Result: UNVERIFIED until the tag/pin-update proposal is observed; Coder was not accessed here.
## Verification limits
- No tests, installs or smoke runs were executed; the assessment is static.
- Whether the TypeSafe skills repository publishes a release tag, and its latest tag and commit, was not checked (no network fetch of that repository). The issue records this as "Not known yet"; the owner's decision selects the pinned route, so the actual tag is the first implementation input.
- GitHub was read with `gh issue view/list` and `gh pr list/view` on IronbellyOrg/IronClaude only, per the brief. No writes were made anywhere.
- The Coder repository's upstream monitor state is UNVERIFIED from this repo; its config lives in IronbellyOrg/PrivateRepoF, out of scope here.
