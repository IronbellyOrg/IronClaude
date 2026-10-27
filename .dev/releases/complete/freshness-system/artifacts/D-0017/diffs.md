# D-0017 — README + CHANGELOG + docs/user-guide/freshness-hooks.md

## Task: T04.05 (EXEMPT)

Three documentation deliverables landed.

## README.md

Added one bullet to the **Highlights** section:

```diff
   - **Contributor workflow support** with source/dev-mirror sync between `src/superclaude/` and `.claude/`
+  - **Context freshness hooks** (v4.3) — eight shell hooks that inject a per-turn `<session-context>` envelope and block edits against files that have not been re-Read since they were last modified. See [`docs/user-guide/freshness-hooks.md`](docs/user-guide/freshness-hooks.md).
```

## CHANGELOG.md (new file)

Created with an `[Unreleased]` entry. Contents:

- Added: Context Freshness System (hooks + `install_hooks.py`), `make sync-dev` hooks, CLAUDE.md discipline section.
- Fixed: `session-init.sh` relative path in `hooks.json` (Option B from `docs/analysis/hooks-json-relative-path-issue.md`).
- Notes: opt-out instructions, user-scope only.

## docs/user-guide/freshness-hooks.md (new file)

Sections:

1. **What gets installed** — 8 hooks table + state-files layout + telemetry path.
2. **Behavioral changes you'll see** — 4 numbered examples of blocks (no_prior_read, read_too_old, external_change, session envelope).
3. **How to opt out** — selective (per-event) and global (delete + remove scripts).
4. **FAQ** — 5 entries: jq dependency, repo-local hooks (no — user-scope only), 30-min tuning, "is it working?" check, settings.json recovery from backups.
5. **Design references** — links back to InfraDocs design + tasklist.

## Acceptance

- Three diffs documented (README, CHANGELOG, docs page).
- Opt-out instructions present in docs page (How to opt out section, selective and global).
- CHANGELOG entry follows the Keep-a-Changelog format (`[Unreleased]` → Added/Fixed/Notes).
