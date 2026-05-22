# Troubleshoot Report — Issue 1: doc_context_card_path null contract ambiguity

**Target**: auggie review #3290499057 on PR #73
**Tier reached**: 1
**Confidence**: 0.97
**Status**: success

## Root cause

`SKILL.md:52` field definition says `doc_context_card_path = null` when "`--no-doc-discovery` was set OR when Wave 1.5 produced no relevant docs across all three branches." But the Wave 1.5 Failure Handling row (`SKILL.md:184`) and the global Error Handling row (`SKILL.md:404`) both override that: when all three branches return no hits, the wave **still writes** an empty "None found" card and **still emits the path**. Authoritative behavior: `null` ONLY when `--no-doc-discovery` skips the wave entirely.

## Proposed Fix

**Edit 1 — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:52`** (Output Contract `doc_context_card_path` row description)

Old:
> When Wave 1.5 ran, the **repo-relative** path of the Documentation Context Card (e.g., `.dev/troubleshoot/bug-foo-20260522/doc-context.md`). `null` when `--no-doc-discovery` was set OR when Wave 1.5 produced no relevant docs across all three branches. Format is repo-relative, same convention as `test_file_path`.

New:
> When Wave 1.5 ran, the **repo-relative** path of the Documentation Context Card (e.g., `.dev/troubleshoot/bug-foo-20260522/doc-context.md`). `null` ONLY when `--no-doc-discovery` was set (the wave is skipped entirely). When the wave runs but produces no relevant docs across all three branches, the field still points to an empty card whose sections all read "None found" — distinguished downstream from the skip case via the hypothesis card's `consistency_with_docs=no_docs_found` value. Format is repo-relative, same convention as `test_file_path`.

**Edit 2 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:19`** (header field description)

Old:
> `**Doc context card**: <repo-relative path to <output-dir>/doc-context.md when Wave 1.5 ran, otherwise null>`

New:
> `**Doc context card**: <repo-relative path to <output-dir>/doc-context.md when Wave 1.5 ran (path is present even if the card's sections all read "None found"); null ONLY when --no-doc-discovery was set>`

## Files that MUST NOT change

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:184` — already canonical
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:404` — already canonical
- Wave 1.5 step 4 synthesis instruction (SKILL.md:167-170) — already produces card on every run

## Risk + Rollback

Very low — pure documentation tightening. No executable code, no agent prompt changes. Rollback = `git revert`.
