Install the TypeSafe Jev agent skill plugin by default with everything else, and make sure the upstream monitor watches it.

## Why

Jev is the TypeSafe System One decision model. Its agent skill is the plugin `typesafe@typesafe-ai` (skill `typesafe-ai`, marketplace repository `typesafe-ai/skills`, MIT licence, version 0.6.2 in the local plugin cache). Today it exists only because it was installed by hand on one machine (`~/.claude/settings.json` has `typesafe@typesafe-ai` enabled and the `typesafe-ai` marketplace known). A new workspace or a fresh `superclaude install` does not have it. It is wanted for the blocker classifier work in IronbellyOrg/IronClaude#552 and for any other typed decision step.

## What exists today (read from the code on 2026-11-15)

- The default plugin set lives in IronClaude: `src/superclaude/cli/user_settings_defaults.json` has `enabledPlugins` (lines 29-37: frontend-design, playwright, notion, dropbox, google-cloud-storage, understand-anything, ponytail@ironclaude), `extraKnownMarketplaces` (lines 38-51: claude-plugins-official and understand-anything, both unpinned) and `ironclaudeMarketplace` (lines 52-70: third-party plugins pinned to a reviewed commit; today only Ponytail v5.3.3). `src/superclaude/cli/install_user_setup.py:206` applies the file; `docs/getting-started/installation.md:389` documents it; `tests/cli/test_install_user_setup.py` covers it. `typesafe` and Jev do not appear in it.
- The upstream monitor lives in IronbellyOrg/Coder and reads IronClaude's file: `.github/upstream-monitor/health.py` fetches `src/superclaude/cli/user_settings_defaults.json` from IronClaude master on every run (`DEFAULTS_URL`, line 34; it reads `extraKnownMarketplaces` and `enabledPlugins` at lines 139-144) and lists the unpinned default plugin sources as watch-only (head commit in the health issue, never a PR). For pinned plugins, the Renovate global config `.github/upstream-monitor/renovate-global.json5` (lines 109-115) rewrites an `ironclaudeMarketplace` entry whose description ends in `vX.Y.Z, pinned by IronClaude`. Doc: Coder `docs/operations/upstream-monitor.md` lines 61-63. Related: Coder#419 (one central upstream monitor) and Coder#478 (BMAD and Ponytail not available globally by default).

So the change belongs in IronClaude (the defaults file, installer tests and docs). No Coder change is expected for watching, because the monitor reads the list from here; confirm that with a monitor run after the merge, and open a Coder follow-up only if it does not list the new source.

## What to build

1. Add the plugin and its marketplace to the IronClaude defaults. Two ways, an owner decision with a recommendation: (a) unpinned, like Understand-Anything: `typesafe@typesafe-ai` in `enabledPlugins` and `typesafe-ai` (repo `typesafe-ai/skills`) in `extraKnownMarketplaces`; the monitor then watches it automatically; (b) pinned, like Ponytail: an `ironclaudeMarketplace` entry with a reviewed release tag and commit and a description ending `vX.Y.Z, pinned by IronClaude`, so Renovate proposes updates. Recommendation: pin if the repository has a release tag to pin, because the skill text steers agents; otherwise start unpinned and watched. Whether the repository has release tags is Not known yet.

**Owner decision, 2026-11-16 (documentation only; branch mapping not verified):** route (b), pinned. Use a pinned Jev version and update the upstream monitor to track Jev upstream. The exact pin and cadence are unspecified. This note installs, configures, stores and sends nothing, and implements nothing.

**Owner answer, 2026-11-16 (second note):** pin the latest release tag and commit; later updates are reviewed through the central upstream monitor; if release tags are not posted, start unpinned and watched. A read-only lookup on 2026-11-16 found git tags `v0.6.2` (commit `302eea662c54`) and `v0.5.7` (commit `65a39f393687`) in `typesafe-ai/skills` and no GitHub Releases, so route (b) applies: the owner confirmed on 2026-11-16 that release tags or plain tags suffice. Nothing is pinned by this note.
2. Update the installer tests and `docs/getting-started/installation.md` for the new default.
3. Verify the monitor: after the change merges, the next Coder health run lists `typesafe-ai/skills` (route a) or Renovate proposes a pin PR (route b).
4. Ship no API key. The skill only gives guidance; calling Jev needs a TypeSafe API key (`TYPESAFE_API_KEY`) that each user supplies. The installer and docs must say so and must not send any data to the API by default.

## Acceptance

- A fresh `superclaude install` enables `typesafe@typesafe-ai` and knows its marketplace.
- Installer tests and docs are updated and pass.
- The upstream monitor lists the new source (or proposes a pin) after the next run.
- No key or secret is added to the repository.

## Out of scope

Obtaining or storing a TypeSafe API key; using Jev in review gates (that is IronbellyOrg/IronClaude#552); changes to Coder unless the monitor check fails.
