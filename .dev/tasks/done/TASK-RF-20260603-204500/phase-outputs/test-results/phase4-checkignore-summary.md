# Phase 4 (F1) git check-ignore Summary

**Date:** 2026-06-03

**Interpretation note:** `git check-ignore -v` reports the LAST matching pattern and exits 0 whenever *any* pattern (including a negation) matches; a `!negation` pattern means the file is NOT ignored. The unambiguous signal is plain `git check-ignore` (no `-v`): **exit 1 = NOT ignored (tracked)**, exit 0 = ignored.

| Path | `-v` matched pattern | plain exit | Expectation | Result |
|---|---|---|---|---|
| `.claude/cache/sc-recommend-lookup.yaml` | `.gitignore:122:!.claude/cache/sc-recommend-lookup.yaml` (negation) | 1 (tracked) | NON-ignored | **PASS** |
| `.claude/cache/sc-recommend-plugin.yaml` | `.gitignore:123:!.claude/cache/sc-recommend-plugin.yaml` (negation) | 1 (tracked) | NON-ignored | **PASS** |
| `.claude/cache/sc-recommend-events.jsonl` | `.gitignore:127:.claude/cache/sc-recommend-events.jsonl` (ignore) | 0 (ignored) | still ignored | **PASS** |

Additionally verified (Step 4.1 safety check): the sync-dev mirrors (`.claude/skills/`, `.claude/commands/sc/`) STAY ignored, and `.claude/settings.json` stays trackable — the `.claude/` → `.claude/*` change preserved all existing ignore behavior. `git status` shows `?? .claude/cache/sc-recommend-lookup.yaml` (would be picked up by `git add`).

**F1 fix is functionally effective.** Raw: `phase4-git-check-ignore.txt`.
