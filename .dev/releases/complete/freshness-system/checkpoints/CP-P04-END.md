# Checkpoint Report — End of Phase 4

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`
**Scope:** T04.01 through T04.05 (install_hooks.py + CLI + Makefile + packaging + docs)
**Generated:** 2026-05-12

## Status

**Overall: Pass**

## Verification Results

- `uv run pytest tests/cli/test_install_hooks.py -v` passes: **13/13** (8 required acceptance cases + 5 bonus).
- `make sync-dev` populates `.claude/hooks/` with 8 mode-0755 hook scripts (7 freshness + session-init); `diff` against `src/superclaude/hooks/scripts/` is clean.
- `uv run python -m build --sdist` and `--wheel` both succeed; tar/unzip listing confirms hooks.json + 7 freshness + 1 session-init ship in canonical and force-include paths.
- README highlights gain a freshness-hooks bullet linking to `docs/user-guide/freshness-hooks.md`.
- New `CHANGELOG.md` with `[Unreleased]` entry covering the freshness system.
- New `docs/user-guide/freshness-hooks.md` covers installation, behavior, opt-out, and FAQ.

## Exit Criteria Assessment

- **Zero pytest failures.** 13 passing.
- **Sub-agent security review** for D-0012 covers (a) atomic write, (b) backup-before-write, (c) malformed-target refusal, (d) force-flag preservation of user hooks, (e) chmod-after-copy, (f) no shell-out. All PASS — see `artifacts/D-0012/evidence.md`.
- **Manual fixture test** confirmed: existing user hooks preserved; 7 freshness registrations added; 8 scripts copied with mode 0755.
- **`~/.claude/` is still NOT modified by any Phase 4 task** (live install belongs to Phase 5).

## Issues & Follow-ups (resolved in this session)

| ID | Description | Resolution |
|---|---|---|
| F8 | Initial `install_hooks` collision logic double-counted source-vs-source registrations sharing a matcher (e.g., the SessionStart pair: session-init.sh + freshness-session-start.sh both default to matcher `*`). The second source entry collided with the first source entry after the first was just added. | Refined collision detection to snapshot `original_target_matchers` and `original_target_signatures` BEFORE the merge loop. Collisions now only fire against user's pre-merge state. Source-vs-source registrations with shared matcher but different inner commands both land. |

## Open follow-ups (carry into Phase 5)

| ID | Description | Resolution path |
|---|---|---|
| F6 | T02.05 FileChanged stdin schema not primary-source verified. | Phase 5 probe step (per task spec): deploy temporary probe handler to `~/.claude/settings.json`, edit a watched file in a live session, capture probe JSON, confirm schema, update `freshness-file-changed.sh` if needed. |
| F7 | `session_id` interpolated into hook-script filenames without sanitization. Defense-in-depth helper `validate_session_id()` exists in `install_hooks.py` but is not called by the hook scripts themselves. | Optional Phase 5 hardening: insert `[A-Za-z0-9_-]+` regex check at the top of each hook script. Low priority (Claude Code session_ids are platform-generated UUIDs). |
| F9 | `reads.jsonl` grows unbounded. Each PreToolUse gate evaluation greps the whole file. Sub-millisecond at 50 entries; <50ms at 10K. | Phase 5+ rotation policy: per design §2.1, keep oldest 3 sessions; document in v1.5 cycle. |

## Evidence

| Deliverable | Path |
|---|---|
| D-0012 (install_hooks.py + sub-agent review) | `TASKLIST_ROOT/artifacts/D-0012/evidence.md` |
| D-0013 (pytest output) | `TASKLIST_ROOT/artifacts/D-0013/test-output.txt` |
| D-0014 (main.py wiring) | `TASKLIST_ROOT/artifacts/D-0014/evidence.md` |
| D-0015 (Makefile sync-dev) | `TASKLIST_ROOT/artifacts/D-0015/evidence.md` |
| D-0016 (packaging sdist + wheel) | `TASKLIST_ROOT/artifacts/D-0016/{evidence.md, sdist-listing.txt, wheel-listing.txt}` |
| D-0017 (README + CHANGELOG + docs) | `TASKLIST_ROOT/artifacts/D-0017/diffs.md` |

## Phase 5 hand-off (for the user)

Phase 5 is the LIVE-INSTALL phase and must be run interactively against `~/.claude/`. Recommended order:

1. **T05.01** — `make sync-dev && uv run superclaude install -f` against the real `~/.claude/`. The install_hooks step creates `~/.claude/settings.json.bak.<UTC-ISO>` before any write; audit `before.json` vs `after.json` per the task spec.
2. **T05.02 GATING** — Test 1 (originating-bug smoke): replay the §5.1 docker-compose.yml drift scenario. PASS gates Tests 2-5.
3. **T02.05 PROBE** (insert after T05.01, before T05.02) — Temporarily wire `freshness-file-changed.sh` body to `cat - > ~/.claude/logs/file-changed-probe-$(date +%s).json; exit 0`. Edit a watched file. Capture schema. Compare to handler's assumed `{path, change_type}`. Update handler if needed. **This is required by T02.05 spec but was deferred from Phase 2 because it requires live Claude Code.**
4. **T05.03** — Tests 2-5.
5. **T05.04** — Wait ≥7 days, then telemetry baseline + 4 memory entries.
