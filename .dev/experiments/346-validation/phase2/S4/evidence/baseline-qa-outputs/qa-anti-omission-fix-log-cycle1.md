# QA Anti-Omission Fix Log - Cycle 1 (Gate 5)

**Status:** Complete
**Date:** 2026-11-08

---

Report path: `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md` (line numbers below are as of the start of this pass, before the edits shifted them).

## Row 5 (A1 O-5) - flagless `--yes` alternative - FIXED

- Source re-read: research 01 lines 102 and 142; installer `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ui.js:800-869` (branch at 807 for the four flags; default branch at 838 seeds `user_name`, `project_name`, `communication_language`, `document_output_language`, `output_folder` only when the existing core config is empty, line 843).
- Section 2.1 "Why the `install.sh:42` flag set matters" paragraph (l.121): added the flagless alternative, the one-flag rule and the cost; qualified "`--output-folder` must stay in every first-use command" to "that passes `--user-name`".
- Section 2.1 FIRST_USE(P) definition (l.292): added a pointer to the alternative (step 3.1, Section 9 row 20).
- Section 3.1 (l.568), Section 4.2 G-07, Section 6.0 common fact 4, Section 8 documents row for `slug-configuration.md` line 53: same qualification or pointer.
- Section 8 step 3.1 (l.1456): added "Alternative flag set, not the plan default" with the seeded keys, the consequence and `[UNVERIFIED - never run]`; the default command is unchanged.
- Section 9: new row 20(a) carries the choice; no owner decision invented.

## Row 7 (A1 O-8a) - `bmad-os-*` and re-install rules - FIXED

- Source re-read (read only): `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ide/_config-driven.js:445-448` (existing skill dir removed before copy), `:499-516` (removal set), `:786-803` (`bmad-os-*` skipped in cleanup); `ide/shared/installed-skills.js:43-48` (`isBmadOwnedEntry` returns false for `bmad-os-*`); `core/installer.js:97-101, 406-425` (`_cleanupSkillDirs` after the IDE step); `catalogue/bmad/install.sh:24` (git pathspec `bmad-*`).
- Section 2.1: new paragraph and 3-row table "`bmad-os-*` skills and the installer's re-install rules" (what a `bmad-*` glob does, what the plan does); created-path rows for `.claude/skills/bmad-*/` and `_bmad/core|bmm` extended.
- FIRST_USE(P) condition 3 now reads "other than `bmad-os-*`" at every statement of it: Section 2.1 definition, Section 2.6 proposal row, Section 3.1, SC-07, Section 4.1 gap row, Section 6.0 common fact 4, Section 8 step 3.2 (with the explanation), Phase 1 decision text, step 7.8. Plan default = count `bmad-*` entries other than `bmad-os-*`; the stricter glob is left as an implementer or owner choice (Section 9 row 20(b)).
- Step 5.3 case (d): added a `bmad-os-x` fixture.
- The seed slug's `install.sh:24` is unchanged by the plan; the report says a tracked `bmad-os-x` would, by reading the pathspec, read as "has BMad" [UNVERIFIED - derived, not run].
- Not changed on purpose: README wording for a manual user ("no `.claude/skills/bmad-*`"), which describes the manual command and not the predicate.

## Row 65 (A3 OM-1) - managed-settings source ranking and `first-wins` - FIXED

- Source re-read: `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/research/web-01-claude-code-user-skills-hooks-and-live-reload.md:137-145` (line 143 carries the ranking, the default `first-wins` and the `ANTHROPIC_BASE_URL` rule, quoted from the managed-settings docs). The documentation page itself was not re-fetched: doc-only, tagged `[UNVERIFIED - doc-only]`.
- Section 5.1 W01-17: added the ranking, default `first-wins`, `managedSourcesBehavior: "merge"` and the consequence that a D2 drop-in is ignored when a higher-ranked source delivers any policy key; workspace `ANTHROPIC_BASE_URL` stays "not established".
- Section 6 Option D "How it works" row 7: ranking added. Option D comparison table, D2 Risk cell (new R6) and D2 Cons cell: consequence added.
- Section 4.2 G-03 row and Section 5.3 G-03 summary row: ranking consequence added. Section 7 Rationale row 5 and the Q-reading table row 5 ("what would change"): ranking added. Section 9 row 15 and register 9.1 G-03: ranking added.
- Section 8 step 4D.6 (l.1520): added the ranking consequence and that taking effect is not proven even if drop-ins may hold hooks. Step text is a caveat, not a new step; no owner decision invented.

## Row 66 (A3 OM-2) - skill-frontmatter hooks in untrusted `-p` folders - FIXED

- Source re-read: web-01:127 (frontmatter hooks register on invocation; project skill hooks register "including in a `-p` run in a folder you haven't trusted"), web-01:156 (absolute sentence "no hook-based option escapes it"), web-01:157 (skills not gated; hooks of a project skill "Used" in `-p` runs). The source disagrees with itself; both are recorded.
- Section 5.1 W01-18 relationship line (the only place with the sentence "no hook-based option escapes it", found by Grep): replaced by "no settings-file hook option escapes it" plus an explicit correction, the frontmatter-hook variant, the caveat that the quoted text concerns project skills (user-level stub UNVERIFIED), and the self-disagreement of web-01. Tagged `[UNVERIFIED - doc-only]`.
- Section 8 step 4D.4: added the settings-file versus frontmatter-hook distinction and "(frontmatter-hook variant: W01-18, ...)".
- Not changed: the statements that settings-file hooks are held back in interactive sessions (W01-18 body, Option D row 7, step 4D.4 first part), which stay true; Section 9 row 15 text, which concerns settings-file hooks.

## Counts

- BLOCKING_COUNT from the consolidated findings: 4 (rows O-5 = 5, O-8a = 7, OM-1 = 65, OM-2 = 66).
- Recoveries applied: 4. Rows not recovered: 0. 4 + 0 = 4.
- MINOR rows and the "Recovery text for pinned-test rows" section were not acted on. JUSTIFIED rows (52, 86, 88, 92) were not touched.
- Also changed: Section 9 gained row 20 (carries the O-5 flag-set choice and the O-8a glob choice as unanswered; the intro now says "Rows 15 to 20"). Owner questions Q1 and Q2 (rows 1 and 2) were not edited and remain unanswered; no new plan step was added; the Section 7 and Section 9 feasibility statement was not edited except for a D2 caveat sentence in Section 7 rationale row 5.
- New doc-only claims are tagged `[UNVERIFIED - doc-only]`; derived-not-run claims are tagged `[UNVERIFIED - derived, not run]` or `[UNVERIFIED - never run]`; every `[synthesis inference: ...]` label was left as is.
- Files edited: the report and this log only. Nothing staged, committed or pushed. Installer files under `/opt/nvm/...` were only read.
