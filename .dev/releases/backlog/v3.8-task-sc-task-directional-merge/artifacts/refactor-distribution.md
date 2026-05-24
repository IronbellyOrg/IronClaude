# Refactor Plan — Distribution Surface (Phase 6 / T06.04)

**Task:** T06.04 — Refactor plans: distribution surface & documentation
**Roadmap Item:** R-022
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Every change row is an eight-column directive that Phase 7 will translate into a concrete file edit / installer code change / Makefile target update against `[src]` first, with `[.claude]` refreshed by `make sync-dev` where applicable.

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — TU-1..TU-8, ME-1..ME-9, R-RULE-06 / R-RULE-10 / R-RULE-11.
- `merge-roadmap.md` (T06.01) — milestone **M5** (distribution surface refresh) and CS-M5-A (`superclaude install` + `make sync-dev` filter rules) + CS-M5-B (documentation refresh, scoped to T06.04's companion file).
- `refactor-sctask-deprecation.md` (T06.03) — donor artifact dispositions: `commands/task.md` **SOFT** (CR-DEP-01 / CR-DEP-02); `skills/sc-task-protocol/` **HARD** (CR-DEP-03 / CR-DEP-04). Distribution rows below must match these decisions.
- `refactor-task-skill.md` (T06.02) — confirms every absorbed TU lands at `[src] src/superclaude/skills/task/SKILL.md`; the installer + sync rules continue installing that skill unchanged.
- `refactor-references.md` (T06.03 companion) § 8 — explicit T06.04 hand-off file inventory.
- `[src] src/superclaude/cli/install_commands.py` (auggie-verified, 163 lines).
- `[src] src/superclaude/cli/install_skills.py` (auggie-verified, 144 lines).
- `[src] src/superclaude/cli/install_skill.py` (auggie-verified, helper used by batch installer).
- `[src] src/superclaude/cli/main.py` (auggie-verified, lines 59–163 wire the installer entry points).
- `[src] Makefile` targets `sync-dev` (lines 107–151) and `verify-sync` (lines 153–247).
- `[src] README.md` (auggie-verified — **zero `/sc:task` / `sc-task-protocol` references**; the distribution README does not name the donor surface).

**Companion artifact:** `refactor-documentation.md` (this task's second deliverable) — covers every doc body that names `/sc:task` or the two-surface model (`docs/user-guide/`, `docs/guides/`, `docs/sprint-cli-deep-dive.md`, `docs/analysis/`, `docs/research/`, `docs/generated/`). README change rows live here because the README is a distribution-surface document, not a user-/developer-guide doc.

**Scope boundary (R-RULE-06 + R-RULE-11):**
- This file covers only the **distribution-surface mechanics**: the `superclaude install` component-install code paths, the `make sync-dev` filter logic, the `make verify-sync` orphan check, the `plugins/superclaude/commands/task.md` plugin distribution stub (stub-body rewrite was staked by `refactor-references.md` CR-REF-08; this file owns the installer-side decision), and the repo-level `README.md`.
- The `/task` skill edits, MDTM frontmatter additions, donor artifact deprecation, reference enumeration, and the user-/developer-/reference-guide doc bodies are out of scope (covered by T06.02, T06.03, and the companion `refactor-documentation.md`).
- This refactor does **not** re-litigate any `rejected-features-ledger.md` REJECT/DEFER entry (cross-checked in § 4).

---

## 0. Side-tagging convention (R-RULE-10) — applied to every operative path

Every distribution-surface path below is tagged `[src]` (source of truth) or `[.claude]` (dev-copy mirror) or `[plugins]` (the `plugins/superclaude/` v5.0 plugin-distribution surface tracked under `src/`'s sibling). Phase 7 edits `[src]` first; `[.claude]` is refreshed by `make sync-dev`; `[plugins]` is hand-edited and committed alongside `[src]` because `plugins/` is a first-class distribution surface, not a sync target.

| # | Path | Side | Verified | Disposition role |
|---|---|---|---|---|
| 1 | `src/superclaude/cli/install_commands.py` | [src] | 163 lines (Read 2026-05-15) | Component installer: copies every `*.md` from `commands/` source dir → `~/.claude/commands/sc/`. Iterates *all* `.md`; current behavior installs the (post-CR-DEP-01) deprecation stub. |
| 2 | `src/superclaude/cli/install_skills.py` | [src] | 144 lines (Read 2026-05-15) | Batch skill installer. `_has_corresponding_command()` (lines 19–29) gates `sc-*` skills against a matching command file; if the gate matches, the skill is **never installed** and any stale copy is removed (lines 60–68). |
| 3 | `src/superclaude/cli/install_skill.py` | [src] | helper (Read 2026-05-15) | Single-skill installer used in a loop by `install_skills.py`; copies one skill directory tree to the target. |
| 4 | `src/superclaude/cli/main.py` | [src] | lines 59–163 (Read 2026-05-15) | `install` CLI entry that orchestrates `install_commands → install_agents → install_all_skills`. |
| 5 | `Makefile` (root) | [src] | `sync-dev` lines 107–151; `verify-sync` lines 153–247 (Read 2026-05-15) | Dev-mirror sync (copies `[src]` → `.claude/`) and drift detector (`verify-sync` fails on any `.claude/skills/NAME` lacking a `src/superclaude/skills/NAME`). |
| 6 | `plugins/superclaude/commands/task.md` | [plugins] | Pre-existing deprecation stub (auggie-verified via CR-REF-08) | v5.0 plugin distribution surface. Currently redirects `/task → /sc:task` (a *previous* deprecation cycle that now points the wrong way). |
| 7 | `README.md` (repo root) | [src] | 0 `/sc:task` matches (grep 2026-05-15) | Top-level distribution README. Currently does **not** name `/sc:task`; no rewrite-of-existing rows are required. |
| 8 | `docs/user-guide/freshness-hooks.md` (referenced from README:40) | [src] | Not modified by this refactor | Linked from README; falls under `refactor-documentation.md` if it carries any donor reference (none in scope today). |

**Drift cross-check.** T06.01 confirmed zero byte-level drift on every `[src]` ↔ `[.claude]` path this refactor touches. Phase 7 must keep `make verify-sync` green throughout the staged commits below.

---

## 1. Column legend (every row carries all eight columns — T06.04 AC #1 + AC #4)

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-DIST-NN`). Cross-referenced from `merge-master.md` (T06.05) and Phase 7 commits. |
| **File path (side-tagged)** | `[src]` / `[plugins]` path (the edit target) and any `[.claude]` mirror that `make sync-dev` refreshes. |
| **Change** | The disposition: `edit-in-place` (modify existing lines); `add code path` (insert a new branch / function); `remove code path` (delete an obsolete branch); `audit` (verification-only row, no separate edit). Compatible with `refactor-sctask-deprecation.md` § 1 vocabulary. |
| **Manifest feature(s)** | The TU-N / ME-N / merge-roadmap M-N / CR-DEP-NN that justifies the row. Confirms one-to-many traceability into the manifest (T06.04 AC #3). |
| **Priority (P0–P3)** | P0 = ship-together with the CR-DEP atomic commits; P1 = direct dependent; P2 = follow-on cleanup; P3 = audit-only. |
| **Effort (XS–XL)** | XS ≤ 5 lines; S ≤ 15; M ≤ 30; L ≤ 60; XL > 60. |
| **Dependencies** | Build-order edges. Most rows depend on a CR-DEP-NN (donor artifact disposition must land first or atomically). |
| **Acceptance criteria** | Observable post-condition (grep returns expected count; `make verify-sync` returns 0; installer dry-run output names the expected components). |
| **Risk assessment** | INV-NN / ME-NN / R-RULE-NN at risk + named mitigation. |

---

## 2. Why the distribution surface needs targeted edits (not a sweeping rewrite)

The current distribution wiring already handles the soft-deprecation of the `/sc:task` command **without code changes** — `install_commands.py` iterates every `.md` in `commands/` source and copies it; the (post-CR-DEP-01) deprecation stub will install automatically. The current wiring also already handles the hard-deprecation of the `sc-task-protocol` skill **partially**: `install_skills.py:_has_corresponding_command()` already excludes `sc-task-protocol` from installation today (because `commands/task.md` exists), so the user-side install never carried it as a standalone skill. The *remaining* distribution problems are:

1. **Orphan removal in `~/.claude/skills/`** — `install_skills.py` lines 60–68 only removes a stale `~/.claude/skills/sc-task-protocol/` if the user has a corresponding command file *and* re-runs `superclaude install`. Users who installed *before* `commands/task.md` existed will not auto-clean. Phase 7 must verify the existing cleanup path still fires post-deprecation-stub. (CR-DIST-01.)
2. **Mirror removal in `.claude/skills/`** — `make sync-dev` (lines 111–124) iterates `src/superclaude/skills/*/` and only **creates / overwrites** target directories; it never **removes** orphans. After CR-DEP-04 deletes `src/superclaude/skills/sc-task-protocol/`, the mirror `.claude/skills/sc-task-protocol/` will linger; `make verify-sync` will then **fail** (lines 176–187 flag `.claude/skills/NAME` lacking a `src/` counterpart). Phase 7 must remove the mirror in the same commit as CR-DEP-04. (CR-DIST-02.)
3. **Plugin stub direction reversal** — `plugins/superclaude/commands/task.md` currently redirects `/task → /sc:task` (pre-existing deprecation pointed the *recipient* at the donor). Post-merge, the file must redirect at `/task` as the canonical surface (or be deleted; § 3 picks "redirect", aligning with CR-REF-08's recommendation). (CR-DIST-03.)
4. **`verify-sync` orphan-rule re-verification** — `make verify-sync` lines 176–187 flag any `.claude/skills/NAME` without a matching `src/superclaude/skills/NAME`. Phase 7 must verify this rule fires correctly for the deleted `sc-task-protocol/` mirror as the deletion-detector. (CR-DIST-04.)
5. **README sanity** — README has zero `/sc:task` references today, so no rewrite-of-existing rows. But the merge is a user-facing surface change; a small "Recent changes" / changelog-cross-link callout is the only README change rows we should consider. (CR-DIST-05, optional.)
6. **Repo-root `PROJECT_INDEX.md`** — already covered by `refactor-references.md` CR-REF-10 (remove `sc-task-unified-protocol/` lines). Not re-authored here.

Five operative rows (CR-DIST-01..05) plus one audit row (CR-DIST-06) are the minimal correct set. The installer code paths require **no Python edits**: the existing `_has_corresponding_command()` gate and the iteration over `*.md` already deliver the correct post-deprecation behavior.

---

## 3. Change rows — distribution-surface edits

Six change rows (CR-DIST-01..CR-DIST-06). Order respects: CR-DEP-03 + CR-DEP-04 → CR-DIST-02 (sync-rule + mirror cleanup must land atomically with the donor-side delete) → CR-DIST-01 / CR-DIST-04 (installer / verify-sync re-verification, post-physical-delete) → CR-DIST-03 (plugin stub, after CR-DEP-01 stub language is canonical) → CR-DIST-05 (optional README callout) → CR-DIST-06 (R-RULE-11 audit).

### CR-DIST-01 — `install_skills.py` post-deprecation behavior verification (audit + smoke test)

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-01 |
| **File path (side-tagged)** | `[src] src/superclaude/cli/install_skills.py` (no source edit). |
| **Change** | `audit` — verify the existing `_has_corresponding_command()` gate (lines 19–29) plus the stale-removal block (lines 60–68) correctly handles the post-CR-DEP combination: `commands/task.md` is the soft-deprecation stub (still exists, so the gate still matches) **AND** `src/superclaude/skills/sc-task-protocol/` is deleted (so `list_available_skills()` no longer returns the donor name to iterate at all). Expected behavior: the donor skill name is dropped from `available` (it isn't iterated), so the stale-removal block on line 62–67 only triggers for users who installed pre-deprecation. Phase 7 must add a regression smoke test in `tests/cli/` exercising both code paths. |
| **Manifest feature(s)** | CS-M5-A (installer behavior post-deprecation); CR-DEP-03 + CR-DEP-04 (the donor-side deletes whose behavior this row verifies); R-RULE-06 (no redundant ceremony — installer carries no special-case for the deprecated skill). |
| **Priority** | **P1** — depends on CR-DEP-03 + CR-DEP-04 landing. |
| **Effort** | **S** — no production-code edit; ~10–15 lines of regression test added to `tests/cli/test_install_skills.py` (a similar test file pattern already exists at `tests/cli/test_install_hooks.py` per git status). |
| **Dependencies** | CR-DEP-03 + CR-DEP-04 (skill body deleted from `[src]`); CR-DEP-01 (stub command file present so the `_has_corresponding_command` gate still matches `task` if a future revival re-introduces the directory). |
| **Acceptance criteria** | (1) `uv run pytest tests/cli/test_install_skills.py` passes with the new test. (2) The test asserts: with `commands/task.md` present (stub) **and** `src/superclaude/skills/sc-task-protocol/` **absent**, `install_all_skills()` returns success, `served_by_command` does **not** list `sc-task-protocol` (because it isn't in `list_available_skills()`), `installed` does not list `sc-task-protocol`. (3) A second test asserts: if a user has a pre-existing `~/.claude/skills/sc-task-protocol/` from an old install, **and** the donor command file is somehow still present (the regression-guard scenario), the existing stale-removal block (`install_skills.py:62-67`) still removes it. (4) `superclaude doctor` (per `make verify`) reports no missing skill after a fresh `superclaude install --force`. |
| **Risk assessment** | **INV at risk:** none direct (installer is read-only against the source tree). **ME at risk: ME-9** if the audit catches a code path that re-introduces `mcp-servers:`/`personas:` advertisement reading (it does not — `install_skills.py` is purely path-based; no frontmatter parsing). **Mitigation:** the regression test pins the behavior. **Secondary risk:** a future installer refactor introduces frontmatter-based gating that could re-read deprecated fields — **mitigation:** the test asserts the **absence** of `sc-task-protocol` from the installer's output, regardless of frontmatter content. **R-RULE-06 risk:** an "if skill_name == 'sc-task-protocol' continue" hard-coded special-case would be carrying donor ceremony forward. **Mitigation:** the row explicitly forbids hard-coded special-cases; the existing generic gate (`_has_corresponding_command`) is the only correct mechanism, and the audit verifies it suffices without modification. |

### CR-DIST-02 — `make sync-dev` orphan removal for `.claude/skills/sc-task-protocol/`

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-02 |
| **File path (side-tagged)** | `[src] Makefile` (the `sync-dev` target, lines 107–151). Mirror that needs cleanup: `[.claude] .claude/skills/sc-task-protocol/SKILL.md`. |
| **Change** | `add code path` — extend the `sync-dev` target with an explicit removal step for `.claude/skills/<name>/` directories whose `src/superclaude/skills/<name>/` no longer exists. Two equivalent shapes are acceptable; Phase 7 picks one: **(a)** `rm -rf .claude/skills/sc-task-protocol` as a one-off explicit line in the Makefile (cheap, surgical, single-purpose). **(b)** a generic prune loop after line 124 of the form `for d in .claude/skills/*/; do name=$$(basename "$$d"); case "$$name" in __*) continue;; esac; [ -d "src/superclaude/skills/$$name" ] || rm -rf "$$d"; done` (general, durable, removes any future orphan automatically). **Recommendation: (b)**, because R-RULE-06 favors mechanism over special-case and the generic loop is the same length as the special-case. |
| **Manifest feature(s)** | CS-M5-A (`make sync-dev` filter rules — extends sync semantics from "create/overwrite" to "create/overwrite/prune-orphans"); CR-DEP-04 (the hard-deprecation row whose `[.claude]` mirror cleanup this row mechanizes); R-RULE-10 (the sync rule must keep both sides in lock-step; without prune, the mirror permanently lags the source). |
| **Priority** | **P0** — must land in the **same commit** as CR-DEP-03 + CR-DEP-04 so `make verify-sync` stays green throughout the deprecation sequence (verify-sync fails today on any `.claude/skills/NAME` lacking a `src/` counterpart — lines 176–187 of `Makefile`). |
| **Effort** | **S** — ~5–8 lines of `make` recipe (one for-loop with a guarded `rm -rf`). |
| **Dependencies** | None upstream (Makefile edit can ship first); ship-together with CR-DEP-03 + CR-DEP-04 (the `[src]` deletes that produce the orphan to prune). |
| **Acceptance criteria** | (1) After `make sync-dev` runs in the CR-DEP-03 + CR-DEP-04 commit, `test ! -d .claude/skills/sc-task-protocol` returns true. (2) `make verify-sync` returns 0 in the same commit. (3) The new prune step does **not** remove any non-orphan directory: `make sync-dev` on a clean tree produces zero deletions; verified by an existing-directory invariant check (e.g., `.claude/skills/task/` survives sync). (4) The prune step skips `__*` directories (e.g., a future `__pycache__` accidentally in `.claude/skills/`) by the same `case` guard used elsewhere in the Makefile. |
| **Risk assessment** | **INV at risk: R-RULE-10 (drift)** — if the prune step is wrong and removes a valid skill, the mirror is broken and `make verify-sync` will catch it (the same orphan-rule check at lines 176–187 reports `MISSING in .claude/skills/`, drift=1). **Mitigation:** the prune predicate is `[ -d "src/superclaude/skills/$$name" ] || rm`, an exact inverse of the verify-sync orphan rule. **Secondary risk:** prune deletes a user-authored eval workspace accidentally placed under `.claude/skills/<name>-workspace/` (against the project's explicit prohibition per CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination"). **Mitigation:** the project's PreToolUse hook in `.claude/settings.json` already rejects such writes; `.gitignore` matches `.claude/skills/*-workspace/`; the prune step is destroying a path that **should not exist** in the first place. The acceptance criterion (3) verifies prune does not touch the `task/` skill (or any other genuine skill). **Tertiary risk:** prune is destructive and re-runnable; if a developer manually adds a skill to `[.claude]` without `[src]`, it disappears on next `sync-dev`. **Mitigation:** the project explicitly forbids editing `[.claude]` directly (CLAUDE.md "Component Sync" + memory `feedback_hooks_source_of_truth.md` rule); the prune behavior enforces that rule mechanically. |

### CR-DIST-03 — `plugins/superclaude/commands/task.md` redirect re-target

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-03 |
| **File path (side-tagged)** | `[plugins] plugins/superclaude/commands/task.md` (the v5.0 plugin-distribution stub; pre-existing deprecation file from an earlier cycle). |
| **Change** | `edit-in-place` — rewrite the body to redirect at `/task` as the canonical command (instead of `/sc:task` / `task-unified.md`). Remove the obsolete `deprecated_by: "task-unified"` and `migration_guide:` frontmatter lines. The file's *purpose* (a deprecation stub for any user invoking the plugin-distributed `/task`) is preserved; the redirect target is updated to match the new canonical surface. Aligns with `refactor-references.md` CR-REF-08's "redirect" recommendation; this row picks that option over the `→ T06.04` defer alternative and authors the eight-column directive. |
| **Manifest feature(s)** | CS-M5-A (plugin-distribution surface); CR-REF-08 (companion reference row that staked the initial body rewrite scope and deferred the installer-side decision to T06.04 — this row closes that loop); CR-DEP-01 (the soft-deprecation stub language for `/sc:task` is canonical; the plugin stub re-uses the same redirect form pointing at `/task`); R-RULE-06 (the file already exists as a deprecation artifact; the rewrite re-uses the existing mechanism rather than inventing new ceremony). |
| **Priority** | **P1** — depends on CR-DEP-01 stub language being settled. Ships in a follow-on commit, not the M4 atomic commit. |
| **Effort** | **S** — frontmatter cleanup (≤ 3 lines removed) + body rewrite (≤ 10 lines replaced). |
| **Dependencies** | CR-DEP-01 (stub language canonical at the source surface); CR-REF-08 (reference row that stakes scope). |
| **Acceptance criteria** | (1) `grep -nE "task-unified\|deprecated_by" plugins/superclaude/commands/task.md` returns no matches. (2) The body contains a single-line redirect identical in shape to CR-DEP-01's deprecation stub (`This command was absorbed into /task on 2026-MM-DD. Use /task.`). (3) The frontmatter retains `name:`, `description:` (rewritten as "Deprecated — see /task"), `category:` (set to `deprecated`), `version:` (bumped). (4) The `category: deprecated` frontmatter is consistent with whatever convention `plugins/superclaude/commands/` uses for other deprecation stubs (Phase 7 verifies via grep across `plugins/`). |
| **Risk assessment** | **INV at risk:** none direct (plugins/ is distribution metadata, not runtime-loaded by the `/task` skill). **R-RULE-11 risk:** an over-eager rewrite re-introduces `mcp-servers:` / `personas:` advertisement on the plugin stub (the v5.0 plugin format may carry such fields). **Mitigation:** the rewrite explicitly removes such fields if present (CR-DEP-05's audit grep extends to `plugins/superclaude/commands/task.md`). **Secondary risk:** double-deprecation confusion (a user lands on the file from a stale link and sees a deprecation pointing at `/task`, but `/sc:task` also redirects to `/task` — two stubs, one target). **Mitigation:** both stubs use identical body text, so the user sees a consistent message regardless of entry point. **Tertiary risk:** the plugin stub is loaded by a hypothetical v5.0 plugin marketplace tool that depends on `deprecated_by:`. **Mitigation:** the v5.0 plugin system is **not yet available** (per CLAUDE.md "Plugin System (v5.0 - Not Yet Available)"); the frontmatter is forward-looking metadata only. If v5.0 ships later and requires `deprecated_by:`, the field is re-added then. |

### CR-DIST-04 — `make verify-sync` orphan rule re-verification (audit)

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-04 |
| **File path (side-tagged)** | `[src] Makefile` (the `verify-sync` target, lines 153–247; specifically the orphan rule at lines 176–187 — `for skill_dir in .claude/skills/*/; do ... if [ ! -d "src/superclaude/skills/$$name" ]; then echo "❌ MISSING in src/superclaude/skills/: $$name"; drift=1; fi`). |
| **Change** | `audit` — no Makefile edit. Verify the existing orphan rule correctly fires for the **deleted** `sc-task-protocol/` mirror, AND verify it does not fire for any other legitimate state. The rule is already correct; this row is the audit row that confirms Phase 7 didn't accidentally regress it. |
| **Manifest feature(s)** | CS-M5-A (`make verify-sync` keeps `[src]` ↔ `[.claude]` in lock-step); CR-DIST-02 (this audit verifies the prune is sufficient by re-running verify-sync); R-RULE-10. |
| **Priority** | **P2** — audit row, follows CR-DIST-02. |
| **Effort** | **XS** — no edit; ≤ 3 lines of CI commentary added to the commit message documenting the verify-sync result. |
| **Dependencies** | CR-DIST-02 (the prune that makes the verify-sync pass). |
| **Acceptance criteria** | (1) In the commit that lands CR-DEP-03 + CR-DEP-04 + CR-DIST-02, `make verify-sync` returns 0. (2) An intentional negative test: a `git stash` of CR-DIST-02 alone (leave the deletes from CR-DEP-03/04 in place, revert the Makefile prune) causes `make verify-sync` to fail with the expected `MISSING in src/superclaude/skills/: sc-task-protocol` line — proving the orphan rule fires when expected. Phase 7 documents this in the commit message; the stash is unstaged before commit. (3) No new orphan paths emerge for any other skill. |
| **Risk assessment** | **INV at risk: R-RULE-10 (drift)**. **Mitigation:** the audit is the gate. **Secondary risk:** Phase 7 skips the negative-test step and commits without proving the orphan rule fires. **Mitigation:** the acceptance criterion (2) makes the negative-test mandatory; reviewer checks the commit message for the documented result. |

### CR-DIST-05 — `README.md` (no change; explicit no-op + rationale)

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-05 |
| **File path (side-tagged)** | `[src] README.md` (repo root). |
| **Change** | `audit` — explicit no-op. The README contains **zero** `/sc:task`, `sc:task`, `sc-task-protocol`, or `task-unified` matches (verified: `grep -cE 'sc:task\|sc-task-protocol\|task-unified' README.md` = 0). The two-surface model is not mentioned. No rewrite-of-existing rows are required. |
| **Manifest feature(s)** | CS-M5-A (README rows affected by deprecation — the affected count is **zero** in this repo; the row is authored for explicit traceability so Phase 7 cannot miss it); R-RULE-11 (no re-litigation — README has nothing to re-litigate). |
| **Priority** | **P3** — audit-only. |
| **Effort** | **XS** — no edit. |
| **Dependencies** | None. |
| **Acceptance criteria** | (1) `grep -cE 'sc:task\|sc-task-protocol\|task-unified' README.md` returns 0 (post-merge, same as pre-merge — the README never named the donor surface). (2) Phase 7 reviewer confirms by re-running the grep. (3) The commit message for the M4 / M5 sequence includes a one-line note "README: no change; donor surface unreferenced." |
| **Risk assessment** | **INV at risk:** none. **R-RULE-11 risk:** none (no edit). **Secondary risk:** a *future* README update mentions the donor surface (e.g., a contributor adds a "v3.x deprecations" callout). **Mitigation:** out of scope for this sprint; if it happens, the next sprint authors the row. |

### CR-DIST-06 — R-RULE-11 audit on all CR-DIST rows

| Column | Value |
|---|---|
| **CR-ID** | CR-DIST-06 |
| **File path (side-tagged)** | All CR-DIST-NN rows above (audit-row over the set). |
| **Change** | `audit` — verify no CR-DIST row silently re-proposes a `rejected-features-ledger.md` REJECT or DEFER entry. Cross-checked in § 4 below. |
| **Manifest feature(s)** | R-RULE-11 (governing all Phase 6 plans). |
| **Priority** | **P3** — audit-only. |
| **Effort** | **XS** — verification only. |
| **Dependencies** | CR-DIST-01..05 (the rows being audited). |
| **Acceptance criteria** | (1) § 4 below lists every `rejected-features-ledger.md` REJECT/DEFER entry and confirms no CR-DIST row re-introduces it. (2) Phase 7 reviewer confirms the audit. |
| **Risk assessment** | **INV at risk: R-RULE-11 (silent re-litigation)**. **Mitigation:** the explicit § 4 cross-check is the gate. |

---

## 4. R-RULE-11 audit — no rejected-features-ledger entry re-litigated by a distribution row

Per T06.04 governing R-RULE-11 (inherited from the merge-roadmap and T06.03), distribution-surface changes may not re-introduce a REJECTed or silently-revive a DEFERred pattern. Audit:

| Ledger entry | Status | CR-DIST row that could re-introduce? | Audit verdict |
|---|---|---|---|
| LR-REJECT-2 (D02 / Layer A `mcp-servers:` advertisement) | REJECTed | CR-DIST-01 (installer audit), CR-DIST-03 (plugin stub rewrite) | Neither re-introduces. CR-DIST-01 is path-based (no frontmatter parsing); CR-DIST-03 explicitly removes `mcp-servers:` if present. **Pass.** |
| LR-REJECT-3 / Row 21 (D09b runtime classifier with keyword tables) | REJECTed | None | No CR-DIST row authors classifier prose. **Pass.** |
| LR-REJECT-7 (D15c per-tier procedure synthesis) | REJECTed | None | No CR-DIST row authors procedure prose. **Pass.** |
| LR-DEFER-4 (D01 `allowed-tools:` enforcement) | DEFERRED (ME-8) | None | Distribution surface does not enforce `allowed-tools:` (the loader does, and the deferral is to a future Rule 6 + loader split). **Pass.** |
| LR-DEFER-5 (D08 header emission) | DEFERRED (ME-7) | None | No CR-DIST row emits a header. **Pass.** |
| All other REJECT/DEFER entries | Various | None | Distribution surface is mechanical (installer paths, sync rules, stub rewrites); does not touch the bound rejections. **Pass.** |

**Audit verdict:** zero ledger entries re-proposed; R-RULE-11 satisfied across all CR-DIST rows.

---

## 5. Consistency check against T06.03 deprecation decisions (T06.04 AC #3)

T06.04 AC #3: "Distribution changes are consistent with the artifact-level deprecation decisions in T06.03."

| T06.03 decision (CR-DEP row) | Corresponding T06.04 distribution row | Consistent? |
|---|---|---|
| CR-DEP-01 (soft-deprecate `commands/task.md`; stub remains) | Installer continues to copy the stub (no CR-DIST edit required; `install_commands.py` iterates `*.md` generically); CR-DIST-03 rewrites the **plugin-side** stub to use the same redirect language. | **Yes** — soft-deprecation + identical stub language across `[src]` and `[plugins]` surfaces. |
| CR-DEP-02 (sync soft-deprecated command to `[.claude]`) | Existing `make sync-dev` copies `[src] commands/task.md` → `[.claude] commands/sc/task.md` unchanged (no CR-DIST edit required). | **Yes** — soft-deprecation mirror sync uses unchanged sync logic. |
| CR-DEP-03 (hard-delete `src/superclaude/skills/sc-task-protocol/SKILL.md`) | CR-DIST-02 adds the `make sync-dev` prune step that removes the `[.claude]` mirror in the same commit. CR-DIST-01 audits the installer's existing exclusion gate. | **Yes** — hard-deprecation produces no orphan after the prune; installer exclusion is gateway-correct. |
| CR-DEP-04 (hard-delete `src/superclaude/skills/sc-task-protocol/__init__.py` + rmdir) | CR-DIST-02 prune removes the `[.claude]` mirror; CR-DIST-04 verifies `make verify-sync` returns 0. | **Yes** — atomic with CR-DEP-04 commit; verify-sync is the gate. |
| CR-DEP-05 (re-affirm `mcp-servers:` / `personas:` advertisement removal) | CR-DIST-03 extends the advertisement-removal grep to `plugins/superclaude/commands/task.md`. | **Yes** — single grep covers both `[src]` and `[plugins]` surfaces. |

**Consistency verdict:** every T06.03 decision has a corresponding T06.04 distribution row or an explicit "no edit required" note. **Pass.**

---

## 6. Disposition summary table

| Distribution surface artifact | Disposition | Justification | CR-DIST row |
|---|---|---|---|
| `[src] src/superclaude/cli/install_commands.py` | **No edit** — existing iteration over `*.md` handles the soft-deprecation stub generically | R-RULE-06: existing mechanism suffices; hard-coded special-case would be donor ceremony forward. | (none — explicit no-op called out in § 2) |
| `[src] src/superclaude/cli/install_skills.py` | **No edit** — existing `_has_corresponding_command()` gate handles the hard-deprecation generically | Same as above; gate already excludes `sc-task-protocol` because `commands/task.md` exists. | CR-DIST-01 (audit) |
| `[src] Makefile sync-dev` (lines 107–151) | **Add code path** — generic orphan-prune loop after line 124 | Sync must keep `[src]` ↔ `[.claude]` in lock-step; without prune, the hard-deprecation produces a mirror orphan that fails verify-sync. | CR-DIST-02 |
| `[src] Makefile verify-sync` (lines 153–247) | **No edit** — existing orphan rule (lines 176–187) already catches the regression scenario | Existing logic is correct; audit row confirms it fires on the right path. | CR-DIST-04 (audit) |
| `[plugins] plugins/superclaude/commands/task.md` | **Edit-in-place** — rewrite redirect from `/task → /sc:task` to `/sc:task → /task` (with frontmatter cleanup) | Pre-existing deprecation pointed at the donor; merge inverts the canonical surface. | CR-DIST-03 |
| `[src] README.md` | **No edit** — README never named `/sc:task` (zero grep hits) | No row to rewrite. | CR-DIST-05 (audit) |

---

## 7. Phase 7 execution-order constraint (within M5)

Ordering (from T06.03 § 7 + this file):

CR-DEP-01 + CR-DEP-02 (atomic, M4-A commit) → CR-DEP-03 + CR-DEP-04 + **CR-DIST-02** (atomic, M4-B commit; the sync-rule extension and the physical deletes coupled so `make verify-sync` stays green) → CR-DIST-01 (audit + regression test, follow-on commit) → CR-DIST-04 (audit, same commit as CR-DIST-02 or follow-on) → CR-DIST-03 (plugin stub rewrite, follow-on; can co-commit with CR-REF-08's referenced rewrite as a single distribution-cleanup commit) → CR-DIST-05 (README no-op, audit note in commit message) → CR-DIST-06 (R-RULE-11 audit across all CR-DIST rows, post-hoc).

**Atomicity rule:** CR-DIST-02 **must** land in the same commit as CR-DEP-03 + CR-DEP-04. Without atomicity, `make verify-sync` fails between the donor-side delete and the mirror-side prune.

The dependency edge from M1+M2+M3 (TU absorption) → M4 (donor deprecation) → M5 (distribution refresh) is the absorption-must-precede-deprecation-must-precede-distribution rule from `merge-roadmap.md` §4. Phase 7 enforces this via the dependency arrows in `merge-master.md` (T06.05).

---

## 8. Acceptance criteria roll-up (T06.04 AC mapping)

| T06.04 AC | Where satisfied in this file |
|---|---|
| **AC #1** — `refactor-distribution.md` exists with change rows for `superclaude install`, `make sync-dev`, and README, all paths auggie-verified and side-tagged | § 0 (side-tagged path table), § 3 (six rows covering installer audit / sync-dev prune / verify-sync audit / plugin stub / README no-op / R-RULE-11 audit). |
| **AC #2** — owned by the companion `refactor-documentation.md` | n/a in this file. |
| **AC #3** — Distribution changes are consistent with the artifact-level deprecation decisions in T06.03 | § 5 (explicit consistency check table). |
| **AC #4** — Every change row carries the standard eight columns including risk assessment | § 3 — all six rows have all eight columns including a risk-assessment cell that names INV-NN/ME-NN/R-RULE-NN and the mitigation. |

---

## 9. Companion artifact handoff

`refactor-documentation.md` (T06.04's second deliverable) consumes the file inventory from `refactor-references.md` § 4.G + § 8. Every doc body that names `/sc:task` or the two-surface model carries a treatment row there. The README is owned by this file (CR-DIST-05); user-/developer-/reference-guide docs are owned by the companion. The two files together close every distribution + documentation surface affected by the merge.
