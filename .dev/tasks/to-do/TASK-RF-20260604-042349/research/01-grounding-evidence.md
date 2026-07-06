# Research: PR #133 critique grounding (pre-completed)

**Topic type:** File Inventory + Doc Cross-Validator
**Scope:** docs/user-guide/{commands.md,flags.md}, src/superclaude/commands/reflect.md, src/superclaude/skills/sc-reflect-protocol/SKILL.md, plugins/superclaude/commands/reflect.md, commands/sc-reflect.md
**Status:** Complete
**Date:** 2026-06-04
**Source:** grounded live this session against `origin/master` (PR #133 = `b9724e49`); local tree is 6 commits behind.

---

## CRITICAL CONTEXT — branch base

`origin/master` carries PR #133's v2 docs. The working tree does NOT (6 commits behind).
**All line numbers below are `origin/master`-relative.** Every edit must branch off
`origin/master` and re-`grep -n` its anchor against the freshly checked-out file. [CODE-VERIFIED]

## C1 — `--tasklist` over-stated as required for post  [CODE-VERIFIED]

- Skill hard-STOP (`src/superclaude/.../SKILL.md` §3.3 / `reflect.md:33`): post STOPs only on
  missing `--diff` AND `--task-log`. **Missing `--tasklist` does NOT STOP.**
- Over-statements to downgrade → "strongly recommended":
  - `docs/user-guide/flags.md:144` — `--tasklist … required for --mode post`
  - `src/superclaude/commands/reflect.md:73` — `Tasklist file. **Required for UC-2**`
  - `src/superclaude/skills/sc-reflect-protocol/SKILL.md:68` — `(required for UC-2; recommended for UC-1 …)`
- **⚠️ ADJACENT `--diff` ROW MUST SURVIVE** (genuine requirement):
  - `flags.md:145` — `--diff … required for --mode post (unless --task-log)`
  - `reflect.md:74` — `--diff … **Required for UC-2** unless --task-log`
  - `SKILL.md:69` — `--diff … (required for UC-2)`
- Already-consistent anchor: `reflect.md:28` says "recommended" for UC-2 (the correct framing).

## C2 — legacy post example lacks --diff  [CODE-VERIFIED]

- `docs/user-guide/commands.md:1024` (origin/master) — `/sc:reflect --type task --validate   # maps to --mode post`.
- Standalone copy-paste STOPs (no diff/task-log). Legacy block header (~:1020) already names Wave 6.
- Fix: additive note that the post-mapped legacy form needs `--diff`/`--task-log`.

## C3 — `--task-log` dead breadcrumb  [CODE-VERIFIED]

- `flags.md:145` references "(unless `--task-log`)" but Reflect table (142-152) has no `--task-log` row.
- `reflect.md:77` defines it: "Task execution log (UC-2 alternative input when no diff is available)."
- Fix: add `--task-log` row to flags table.

## C4 — flags table missing PR-headlined flags  [CODE-VERIFIED]

- `reflect.md:86` `--no-verify`, `:87` `--onboard`, `:88` `--with-hierarchy` — all real.
- `flags.md` Reflect table omits them. Table is curated (omits ~15 other flags) → add only these 3 + pointer.

## C5 — duplicate copies stale at v1  [CODE-VERIFIED]

- `plugins/superclaude/commands/reflect.md:22` — v1 `--type task|session|completion`.
  Provenance: Priority-2 install source (`src/superclaude/cli/install_commands.py:112-116`). Real risk.
- `commands/sc-reflect.md` — v1 + corrupted heading `# /sc:sc:sc:reflect` and body `/sc:sc:reflect …`
  (from `465797ad` namespace-isolation sync). NOT install-resolved (orphan).
- Decision (user 2026-06-04): keep + sync BOTH to v2; fix `/sc:sc:` prefix in the root copy.
- `make sync-dev` copies `src/superclaude/{skills,agents}` → `.claude/` ONLY (Makefile:111). It does NOT
  touch `plugins/` or root `commands/` — both are hand-maintained. [CODE-VERIFIED]

## Integrity (R6)

- `make verify-sync` gates skills/agents sync; run after T-002/T-003 touch src/.
- Never stage `.claude/**` except settings.json (CLAUDE.md ABSOLUTE).
- PR target: `gh pr create --repo IronbellyOrg/IronClaude --base master` only.
