# Documentation Context Card

**Generated**: 2026-11-04T16:20:12Z
**Wave**: 1.5
**Scope**: src/superclaude/cli/install_user_setup.py:332

## Release context

No .dev/releases hit. Issue-330 FR-002 pins Ponytail to one named source, "No other repo is accepted" (.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md:36); the plan accepted a key-only known_marketplaces guard (:161); R-6 names the supply-chain risk (adversarial/variant-1-opus-architect.md:164). The pin proof (m2-pin-proof.md) covers only fresh HOMEs.

## Architectural docs consulted

- docs/getting-started/installation.md (current): Ponytail only at the pinned commit through IronClaude's own ironclaude marketplace (:370-379); plugin failures never fail the install (:357-360). Silent on a pre-existing ironclaude registration and on failed add/update.
- CHANGELOG.md (current): same promise (:13), same silence.

## Restrictions / decisions that constrain the fix

- Plugin step stays non-fatal (install_user_setup.py:38, :287; installation.md:358).
- Ponytail only from the pinned, IronClaude-owned catalog (install_user_setup.py:17; installation.md:370).
- Never remove or overwrite a marketplace the user may own (install_user_setup.py:10; installation.md:399): the installer must not silently remove a foreign ironclaude marketplace.

## Re-frame signals

- The pin is only as strong as the marketplace binding: trusting the name alone breaks the promise at installation.md:370.
- The safe response to a mismatch is to refuse (report and skip Ponytail), not to rebind, because removing a user's marketplace uninstalls its plugins.
- A failed add/update must stop the commands that depend on that marketplace.
