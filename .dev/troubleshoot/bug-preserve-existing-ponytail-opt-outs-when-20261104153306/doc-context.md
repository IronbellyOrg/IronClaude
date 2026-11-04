# Documentation Context Card

**Generated**: 2026-11-04T15:34:32Z
**Wave**: 1.5
**Scope**: src/superclaude/cli/user_settings_defaults.json:36

## Release context

No .dev/releases artifact covers these components. The issue-330 brainstorm and plan guarantee the opt-out: "ponytail@ponytail": false must stay false and no Ponytail command may run after a rerun (.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md:170, :287; .dev/tasks/done/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md:44, :81). They predate the rename to ponytail@ironclaude (1de47e82).

## Architectural docs consulted

- docs/getting-started/installation.md (current): defaults fill only keys you have not set (:345); opt-out is "ponytail@ironclaude": false (:458); after #358 both copies end up enabled (:393-411). Silent on an earlier "ponytail@ponytail": false.
- CHANGELOG.md (current): same opt-out (:11) and migration text (:14); silent on carrying the old opt-out over.

## Restrictions / decisions that constrain the fix

- install_user_setup.py:10 "a person's own choices are never overwritten" (merge fills only missing keys).
- install_user_setup.py:281 / installation.md:356: install only plugins the user has not disabled.
- installation.md:398 / CHANGELOG.md:14: the installer leaves ponytail@ponytail itself alone (coordinator decision: do not remove or disable an entry IronClaude cannot prove it added).

## Re-frame signals

- The user's intent ("no Ponytail") is recorded under the old key; the per-key merge honours the key, not the intent, so the opt-out is lost on rename.
- A fix that only reads the old key's false (never writes or deletes it) stays inside "never overwrite" and "leave ponytail@ponytail alone".
- Docs/CHANGELOG must then say the old false carries over (branch C note on installation.md:458, CHANGELOG.md:11).
