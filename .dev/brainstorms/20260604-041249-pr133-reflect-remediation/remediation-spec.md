# Spec — PR #133 Review-Critique Remediation

**Driving authority (ground truth):** the canonical `/sc:reflect` surface as defined in
`src/superclaude/commands/reflect.md` (v2.0.0) and `src/superclaude/skills/sc-reflect-protocol/SKILL.md`.
Documentation MUST match the **enforced** behavior of that surface, not aspirational wording.

**Source of critiques:** 5 `augmentcode[bot]` review suggestions on merged PR #133
(`docs(sc-reflect): align command + user-guide docs with v2.0.0 tiered protocol surface`),
verified against `origin/master` (local tree is 5 commits behind; PR #133 = commit `b9724e49`).

**Branch base:** all remediation branches off `origin/master` (the only ref carrying PR #133 content).

---

## Ground-truth invariants (the arbiter for every requirement)

- **GT-1 (post hard requirement):** `/sc:reflect --mode post` STOPs only when **both** `--diff` and
  `--task-log` are absent (`reflect.md:33`, `SKILL.md §3.3`). Missing `--tasklist` does **NOT** STOP.
- **GT-2 (tasklist status):** `--tasklist` is, in enforced reality, *recommended* for post — not required.
  `reflect.md:28` already says "recommended"; `reflect.md:73` + `flags.md:144` + `SKILL.md:68` wrongly say "required".
- **GT-3 (real flags):** `--task-log` (`reflect.md:77`), `--no-verify` (`reflect.md:86`), `--onboard`
  (`reflect.md:87`), `--with-hierarchy` (`reflect.md:88`) are all real, documented flags.
- **GT-4 (install source):** `plugins/superclaude/commands/` is a Priority-2 install source
  (`install_commands.py:112-116`). Root `commands/` is NOT in install resolution and NOT the
  `build-plugin`→`dist/` output (orphan).

---

## Requirements

### R1 — `--tasklist` wording reflects enforced behavior (resolves C1, medium)
The "required for `--mode post`" claim MUST be downgraded to "strongly recommended" wherever it appears,
so docs match GT-1/GT-2. Post examples that omit `--tasklist` are then correct and need no change.
- **AC-R1.1:** `docs/user-guide/flags.md` `--tasklist` row no longer says "required for `--mode post`".
- **AC-R1.2:** `src/superclaude/commands/reflect.md:73` no longer says "Required for UC-2".
- **AC-R1.3:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md:68` no longer says "required for UC-2".
- **AC-R1.4:** No post example is mutated solely to satisfy a wording claim (the wording is the defect).

### R2 — legacy post example clarifies required inputs (resolves C2, medium)
The legacy `--type task --validate` (→ post) example MUST note that `--diff`/`--task-log` are still
required, and that `/sc:troubleshoot` Wave 6 supplies them (standalone callers add `--diff`).
- **AC-R2.1:** `docs/user-guide/commands.md` legacy block carries an explicit `--diff`/`--task-log` note.
- **AC-R2.2:** The note names the Wave 6 caller as the input source.

### R3 — `--task-log` documented in flags table (resolves C3, low)
The `flags.md` Reflect table MUST include a `--task-log` row so the "(unless `--task-log`)" reference
is not a dead breadcrumb (GT-3).
- **AC-R3.1:** `docs/user-guide/flags.md` Reflect table has a `--task-log` row with its UC-2-alternative purpose.

### R4 — PR-headlined flags documented (resolves C4, low)
The `flags.md` Reflect table MUST add the three PR-headlined flags (`--no-verify`, `--onboard`,
`--with-hierarchy`) plus a pointer that the table is a curated subset (full surface in the command file).
- **AC-R4.1:** Rows present for `--no-verify`, `--onboard`, `--with-hierarchy`.
- **AC-R4.2:** A "full flag surface → command reference" pointer is present (sets curation expectation;
  avoids implying the table is exhaustive).

### R5 — duplicate command copies no longer mislead (resolves C5, medium)
The live install-fallback copy MUST be brought to v2; the orphan copy MUST be explicitly dispositioned.
- **AC-R5.1:** `plugins/superclaude/commands/reflect.md` reflects the v2 `--mode` surface (no v1 `--type
  task|session|completion` as the primary grammar; legacy mapping preserved).
- **AC-R5.2:** Root `commands/sc-reflect.md` is synced to the v2 `--mode` surface AND its
  `/sc:sc:sc:reflect` / `/sc:sc:reflect` prefix corruption is corrected to `/sc:reflect`
  (user decision 2026-06-04: keep + sync, not delete).

### R6 — sync + lint integrity (cross-cutting, non-negotiable)
- **AC-R6.1:** Any edit to `src/superclaude/{commands,skills}/**` is followed by `make sync-dev` + `make verify-sync`.
- **AC-R6.2:** `.claude/**` (except settings.json) is never staged.
- **AC-R6.3:** Changed markdown passes repo markdownlint (inline-disable for pre-existing MD040/MD051 per PR #133 precedent).
- **AC-R6.4:** No PR is opened against upstream; target is `IronbellyOrg/IronClaude` with explicit `--repo`.

### R7 — branch base + anchor integrity (gating, from reflect-pre G3)
The working tree is NOT on `origin/master` (it is 6+ commits behind; PR #133 content is absent). All
line anchors below are `origin/master`-relative.
- **AC-R7.1:** A new branch `docs/pr133-reflect-critique-remediation` is cut from `origin/master`
  (`git fetch origin && git checkout -b … origin/master`) BEFORE any edit.
- **AC-R7.2:** Every edit re-confirms its anchor against the freshly checked-out file
  (`grep -n`) — never trusts the origin/master line number blindly.

### R8 — surgical wording edits (from reflect-pre G-ANCHOR, critical)
`"required for UC-2"` appears on BOTH the `--tasklist` row AND the adjacent `--diff` row in
`SKILL.md` (68/69) and `reflect.md` (73/74). The `--diff` requirement is genuine and MUST survive.
- **AC-R8.1:** The C1 wording downgrade touches ONLY the `--tasklist` row in each file.
- **AC-R8.2:** Post-edit verification confirms the `--diff … required for UC-2` text is unchanged.
