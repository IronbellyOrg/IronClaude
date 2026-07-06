---
title: PR #133 reflect-critique remediation
spec: ./remediation-spec.md
branch_base: origin/master
branch: docs/pr133-reflect-critique-remediation
---

# Tasklist — PR #133 Review-Critique Remediation

All line numbers are `origin/master` (PR #133 = `b9724e49`). Branch off `origin/master` first.

## T-000 — Branch off origin/master + re-anchor (GATING)  → R7 (AC-R7.1, AC-R7.2)
**Action:** `git fetch origin && git checkout -b docs/pr133-reflect-critique-remediation origin/master`.
The working tree is on an unrelated branch 6+ commits behind origin/master; PR #133 content is absent here.
Then re-`grep -n` every anchor below against the freshly checked-out files before editing (do NOT trust the
origin/master line numbers blindly).
**Risk:** high if skipped — every edit below mis-targets. Blocks T-001..T-011.

## T-001 — Downgrade `--tasklist` wording in flags.md  → R1 (AC-R1.1), R8
**File:** `docs/user-guide/flags.md` (Reflect table, `--tasklist` row, ~line 144)
**Edit:** `Path — **required for `--mode post`**` → `Path — **strongly recommended for `--mode post`** (does not STOP if omitted)`
**Risk:** none (wording only).

## T-002 — Downgrade `--tasklist` wording in canonical command file  → R1 (AC-R1.2), R8
**File:** `src/superclaude/commands/reflect.md` (Options table, `--tasklist` row, ~line 73)
**Edit (TASKLIST ROW ONLY):** `Tasklist file. **Required for UC-2** (recommended for UC-1 when one exists).`
→ `Tasklist file. **Strongly recommended for UC-2** (does not STOP if omitted; the post hard requirement is `--diff` or `--task-log`). Recommended for UC-1 when one exists.`
**⚠️ DO NOT touch the adjacent `--diff` row (~:74) — `--diff … **Required for UC-2** unless --task-log` is genuine and MUST survive (R8/G-ANCHOR).**
**Verify after:** `grep -n "Required for UC-2" src/superclaude/commands/reflect.md` still shows the `--diff` row.
**Risk:** low if surgical; corrupts the STOP contract if blanket-replaced.

## T-003 — Downgrade `--tasklist` wording in skill source  → R1 (AC-R1.3), R8
**File:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (`--tasklist` line — verified `:68` in current src/ tree)
**Edit (TASKLIST LINE ONLY):** `--tasklist <path> — tasklist file (required for UC-2; recommended for UC-1 ...)`
→ `--tasklist <path> — tasklist file (strongly recommended for UC-2 — does not STOP if omitted; recommended for UC-1 ...)`
**⚠️ DO NOT touch line `:69` — `--diff <ref-or-path> — … (required for UC-2)` is genuine and MUST survive (R8/G-ANCHOR).**
**Verify after:** `grep -n "required for UC-2" SKILL.md` still shows the `--diff` line.
**Risk:** low if surgical. **Triggers T-009 sync.**

## T-004 — Clarify legacy post example inputs  → R2 (AC-R2.1, AC-R2.2)
**File:** `docs/user-guide/commands.md` (after the legacy grammar block, ~line 1024)
**Edit:** add note: `> The post-mapped legacy form (`--type task --validate`) still requires `--diff` or `--task-log`. `/sc:troubleshoot` Wave 6 supplies these; standalone callers must add `--diff <ref>`.`
**Risk:** none (additive note).

## T-005 — Add `--task-log` row to flags table  → R3 (AC-R3.1)
**File:** `docs/user-guide/flags.md` (Reflect table)
**Edit:** add row `| `--task-log` | Completed work to audit (UC-2 alternative to `--diff`) | Path |`
**Risk:** none (additive). Also removes the C3 dead breadcrumb.

## T-006 — Add PR-headlined flags + curation pointer  → R4 (AC-R4.1, AC-R4.2)
**File:** `docs/user-guide/flags.md` (Reflect table + a pointer line)
**Edit:** add rows for `--no-verify` (disable UC-2 verification triangle), `--onboard` (opt-in Serena cold-start), `--with-hierarchy` (opt-in type_hierarchy); add pointer: `Full flag surface: see `src/superclaude/commands/reflect.md`.`
**Risk:** none (additive). Scope-bounded to the 3 headlined flags (NOT all ~25).

## T-007 — Sync install-fallback copy to v2  → R5 (AC-R5.1)
**File:** `plugins/superclaude/commands/reflect.md`
**Edit:** replace v1 `--type task|session|completion` primary grammar with the v2 `--mode pre|post` surface (mirroring canonical `reflect.md`); preserve legacy mapping section. Match the plugins-copy template structure (do not blind-copy the 265-line canonical file).
**Risk:** medium — manual content port; verify against canonical surface after edit.

## T-008 — Sync orphan root copy to v2 + fix prefix corruption  → R5 (AC-R5.2)
**File:** `commands/sc-reflect.md`
**Action (user decision 2026-06-04: keep + sync):** bring to the v2 `--mode pre|post` surface (mirroring canonical `reflect.md`, matching this copy's template structure), AND correct the prefix corruption — heading `# /sc:sc:sc:reflect` → `# /sc:reflect`, and all `/sc:sc:reflect …` body occurrences → `/sc:reflect …` (the `/sc:` double/triple-prefix came from the `465797ad` namespace-isolation sync).
**Verify after:** `grep -n "sc:sc:" commands/sc-reflect.md` returns nothing; `--type task|session|completion` no longer the primary grammar.
**Risk:** medium — manual port + prefix correction; verify no residual `/sc:sc:`.

## T-009 — sync-dev + verify-sync  → R6 (AC-R6.1)
**Action:** `make sync-dev && make verify-sync` (required because T-002/T-003 touch `src/superclaude/{commands,skills}`).
**Risk:** none.

## T-010 — Lint changed markdown  → R6 (AC-R6.3)
**Action:** run repo markdownlint on changed `.md`; inline-disable pre-existing MD040/MD051 per PR #133 precedent (no new debt).
**Risk:** none.

## T-011 — PR to fork  → R6 (AC-R6.4)
**Action:** `gh pr create --repo IronbellyOrg/IronClaude --base master --head docs/pr133-reflect-critique-remediation ...`. Never bare `gh pr create`. Verify returned URL is `IronbellyOrg/IronClaude`.
**Risk:** none (guarded). **Never stage `.claude/**` (except settings.json).**
