# Troubleshoot Report

**Target**: Verified Codex finding on PR #360 (src/superclaude/cli/user_settings_defaults.json:36): a "ponytail@ponytail": false opt-out does not carry over to "ponytail@ironclaude"
**Type**: bug
**Tier reached**: 1
**Confidence**: 1.00
**Status**: success
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/troubleshoot/bug-preserve-existing-ponytail-opt-outs-when-20261104153306/doc-context.md
**Duration**: 420
**Date**: 2026-11-04T15:39:52Z

---

## Summary

A user who opted out of Ponytail with master's documented `"ponytail@ponytail": false` gets `"ponytail@ironclaude": true` added on the next `superclaude install` or `update`, and install_plugins then selects the pinned Ponytail for install. The defaults merge fills each missing key independently and never reads the plugin's old id. Fix: when filling `ponytail@ironclaude`, carry over an existing `ponytail@ponytail: false`; never edit the old key, never override an explicit new-key value.

## Documentation Context

- **Relevant refs**: .dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md, docs/getting-started/installation.md, CHANGELOG.md, src/superclaude/cli/install_user_setup.py (docstring)
- **Documented behavior**: defaults fill only keys you have not set; the opt-out is a false enabledPlugins value; issue-330 AC-M2 requires an opt-out to survive reruns.
- **Restrictions honored**: never overwrite a user's value (install_user_setup.py:10); leave ponytail@ponytail itself alone (installation.md:398).
- **Restrictions overridden**: None (docs gain one sentence on the carry-over).
- **Card path**: /home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/troubleshoot/bug-preserve-existing-ponytail-opt-outs-when-20261104153306/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

The "Settings defaults: added" message names every added key and always reaches stdout.
It does not show that the plugin was already disabled under its old id.
No effect on this diagnosis: the local repro observed the exact failing state (verdict capped to partial only because auggie was unavailable).

(Full card: /home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/troubleshoot/bug-preserve-existing-ponytail-opt-outs-when-20261104153306/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/troubleshoot/bug-preserve-existing-ponytail-opt-outs-when-20261104153306/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: apply_settings_defaults fills the renamed key `ponytail@ironclaude` with the shipped `true` because its only guard is "this exact key is missing"; an existing `"ponytail@ponytail": false` is never consulted.

**Cause class**: Logic regression (rename of a defaults key without migrating the user's value)

**Detailed explanation**: The rename to `ponytail@ironclaude` (commit 1de47e82) created a key no existing user has. The nested merge writes the default for it (Evidence 1, 2), and install_plugins then selects every default plugin whose value is exactly true (Evidence 3), so the pinned Ponytail is selected for install against the user's opt-out (Evidence 4).

## Evidence

1. `src/superclaude/cli/install_user_setup.py:175` — `for name, entry in value.items():` then `if name not in current:` (:176) and `current[name] = entry` (:177): the guard checks only the key's own name.
2. `src/superclaude/cli/user_settings_defaults.json:36` — `"ponytail@ironclaude": true`
3. `src/superclaude/cli/install_user_setup.py:297` — `wanted = [p for p in defaults.get("enabledPlugins", {}) if enabled.get(p) is True]`
4. Command: `timeout 120 uv run python /tmp/t14c-repro/repro.py` (throwaway HOME, settings `{"enabledPlugins": {"ponytail@ponytail": false}}`) → `ponytail entries after defaults: {'ponytail@ponytail': False, 'ponytail@ironclaude': True}` and `install_plugins would want ponytail@ironclaude: True` (captured in /home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/troubleshoot/bug-preserve-existing-ponytail-opt-outs-when-20261104153306/tier1-observation.md)

## Proposed Fix

Add `_RENAMED_PLUGINS = {"ponytail@ironclaude": "ponytail@ponytail"}` and, in the enabledPlugins fill, write `False` for a missing new id whose old id is literally `False`. The old key is only read. An explicit new-key value is untouched by the existing missing-key guard. An old `true` keeps the documented both-enabled migration.

**Files to change**:
- `src/superclaude/cli/install_user_setup.py` — constant plus a two-line condition in the nested fill loop
- `tests/cli/test_install_user_setup.py` — new regression test
- `docs/getting-started/installation.md`, `CHANGELOG.md` — one sentence each: an existing `"ponytail@ponytail": false` carries over

**Test to verify**:
- add new test: `{"ponytail@ponytail": false}` → `ponytail@ironclaude` is False and the old key unchanged; an explicit `ponytail@ironclaude: true` stays true; an old `true` gives `ponytail@ironclaude: true`.

**Apply with**: applied by the caller (sc:pr-submit S3_FIXING).

## Risk + Rollback

- **Likelihood of regression**: low in apply_settings_defaults (only a missing renamed key whose old value is literally false changes)
- **Test coverage of the changed code**: good after the new test
- **Rollback**: revert the fix commit

## Follow-up tasks

- A workspace that already ran this unmerged branch keeps a saved `ponytail@ironclaude: true`; it cannot be told from a user's choice (PR #360 unmerged, so master users are not exposed). Suggested type: docs.

## Grounding Gaps

- MCP `auggie` was unavailable; grounding and all branch searches used Grep/Read (codegraph fresh for callers).
- The repro script was removed after the run; its captured stdout in tier1-observation.md is the record.
- The repro recomputed install_plugins' `wanted` expression; install_plugins itself (which calls the claude CLI) was not run.

## Next Steps

- Tier 1, high confidence: the caller (sc:pr-submit) applies the fix and runs the new test.

## Pipeline Hardening Closure

pipeline_hardening_applicable=false; pipeline_hardening_verdict: not_applicable. HC0 boundary scan: CLI/subprocess no (pure merge function); file/stdin/prompt delivery no; generated-artifact parser no; gate/severity/status enum no; duplicated evaluator no (install_plugins reads the merged value, single writer); persisted/resume pipeline state no (user settings, not pipeline state); review/audit selector no; sibling pipeline no; prior-escape unmask no.
