# QA Fix Log, Phase 5 (Gate 2 synthesis quality), fix cycle 1

**Status:** Complete
**Date:** 2026-11-08
**Input:** `qa/qa-consolidated-findings-phase5.md` (BLOCKING_COUNT 8; only Blocking = yes rows 1 to 8 are acted on)

---

## Finding 1 (F-04 unguarded manual command): FIXED

- Re-read: `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14` carries the literal unguarded `bmad install --yes --directory . ...`; `catalogue/bmad/install.sh:22-25` is the only guard and it applies to the boot path.
- `synth-04` step 2.2: added the user-facing condition "run only in a project with no `_bmad/` and no `.claude/skills/bmad-*`; if `_bmad/` exists the command updates it with the image's 6.9.0 installer, no version test" (R01 F5-D, F5-F; `ui.js:233-262`), and stated that this is wording, not a technical guard.
- `synth-04` step 2.5: same condition carried to the welcome-text rewording.
- `synth-04` gap-to-step map, F-04 row: now names steps 2.2 and 2.5 for the manual command and keeps 3.2 and 3.3 for the automated path.
- `synth-02` F-04 Notes and SC-07 Status: say the manual command is closed by wording only; SC-07 is met for the new mechanism only.
- No evidence was invented; whether to ship a guarded form of the manual command is stated as not researched.

## Finding 2 (`orca_retirement` "removes only" symlinks): FIXED

- Re-read `templates/VSCode-AIDev02/modules.tf:98-106`: lines 102-104 `rm -f` the `~/.claude/skills/<s>` and `~/.augment/skills/<s>` links only when `readlink` equals `../../.agents/skills/<s>`; line 105 is `rm -rf "$HOME/.agents/skills/$s"`, unconditional, for `orca-cli` and `orchestration`.
- Corrected in every occurrence found by Grep over `synthesis/`: `synth-01` line 220 (writer table), `synth-04` 4B.5, 7.3 and (v)(3) 4B row. Each now cites `modules.tf:101-104` as the conservative-delete precedent and names line 105 as an unconditional `rm -rf` that is not a precedent.
- Left unchanged as accurate: `synth-01` line 173 and `synth-04` Section 9 row 7 say only that orca_retirement removes the skills on deselection.
- Note: research file 02 line 280 ("removes exactly those links") has the same imprecision; research files are read-only, so it was not edited and the synth text follows the code.

## Finding 3 ("pure exec stand-in" comment): FIXED

- Re-read `templates/VSCode-AIDev02/image/Dockerfile.coder:133-135`: the comment says the wrapper is a file and not a symlink because the bin is a `#!/usr/bin/env node` script and NVM node is not on the default PATH. The phrase "pure exec stand-in" is not in it (it is research file 02 line 294, carried over unchecked).
- `synth-03` Option C Cons: phrase removed; now states what the comment says and that one added line would be needed.
- `synth-04` step 4C.1: replaced "the comment ... calling it a pure exec stand-in must be updated" with "extend the comment at `Dockerfile.coder:133-135` ... with one line that the wrapper now also runs the first-use block for the chosen subcommands".
- Verified by Grep over `synthesis/`: 0 remaining matches for "pure exec" or "stand-in".

## Finding 4 (welcome text called unconditional): FIXED

- Re-read `catalogue/bmad/manifest.yaml:12-13`: "If this workspace has a seed repo, BMad is already set up there ..." is conditional on a seed. The real defect is narrower: it ignores the install guards (`install.sh:22-25`: seed not a git work tree, existing `_bmad/`, tracked `bmad-*` skills) and a failed install (`install.sh:41-46`).
- Restated in all places found by Grep: `synth-01` line 146; `synth-02` F-09 and CC-12; `synth-03` Option A Cons and Stage 0 item (b); `synth-04` step 2.5 (title and text) and the Evidence Trail R02 summary row.
- `synth-04` step 2.5 now names a concrete rewording ("BMad is set up there at boot unless that repo already had BMad files") and no longer says "unconditional" or "without a seed". Grep over `synthesis/` shows no remaining claim that the sentence is unconditional.

## Finding 5 (Option F listed as a certain break): FIXED

- Re-read `synth-02` SC-06 (line 68) and G-25 (line 149) and `synth-03` Option F text and Table 1 F column: F has no code path ("None (no code path)"; file 04's X cells void, G-25), so it cannot run from `install.sh`. Evidence base: R01 s2 and s5 (zero consumers of `global_target_dir`).
- F removed from every certain-break list, with E kept conditional ("only if run from `install.sh`", write set UNVERIFIED) and a single statement that F's X cells are void (G-25): `synth-01` impact-summary row, the pinned-tests row in the reconciliation table, the section 2.4 reconciliation sentence, and the contradiction row 3; `synth-02` SC-06, the SC-13 paragraph and F-06 (row title and text); `synth-03` Evidence Trail row for file 04; `synth-04` Phase 5 intro and Table 5.1 `test-57:450` row.
- Left as accurate: `synth-02` K-01 and G-25, `synth-03` Option F text, Table 1, Section 7 row 2.

## Finding 6 (Option C for the CLI reading incoherent; 4C.2 intercepts `status` and `uninstall`): FIXED

- Re-read `synth-03` Section 7 row 1 and Option C step 2 (the wrapper must pass `bmad install`, `--version`, `--help` unchanged: `test-19:1175-1190, 545-561`; `install.sh:18, 42`; `manifest.yaml:25`) and `synth-04` branch table and 4C.2. The old text recommended "Stage 0 plus C in place" while admitting C adds value only for other subcommands or a new name, and 4C.2 made the wrapper install on `status` or `uninstall`.
- Decision applied (the one the finding names; no owner decision invented): for reading (a) the existing `bmad install` already satisfies first use, so the recommendation is Stage 0 only; C is built only if the owner asks for a new, separately named command, which is put to the owner as a sub-question of Q2 in Section 9 row 2.
- `synth-03`: Option C step 2, Table 1 "Which reading" cell for C, Section 7 diagram line (1), Section 7 Stage 1 text, Rationale 6, "Dependence on the owner readings" row 1.
- `synth-04`: Plan basis, Phase 4 intro ("at most one"), branch-table row 1, step 4C.2 (all `status` and `uninstall` interception deleted, with the reason), Section 9 row 2 (a), Integration Checklist line on the branch.
- Grep for "uninstall" over `synthesis/` shows only the explanatory mentions and the rollback note in step 7.6.

## Finding 7 (Q2(b) "BMAD slash skill" mapped to a mechanism the plan cannot give): FIXED

- Re-read `synth-03` Limits row 1, Table 1 B1 "Which reading" cell and `synth-04` step 3.6 / branch table: B gives only the stub's own name; step 3.6 forbids a `bmad-` prefix (W01-2: a personal skill outranks a same-named project skill, doc-only), so `/bmad-help` or any `/bmad-*` still gets nothing in a never-BMAD project.
- Q2(b) reworded as "invoking a named bootstrap skill", with the task-file wording ("a BMAD slash skill") kept in parentheses for traceability. The owner question stays unanswered.
- Added the sentence that a literal `/bmad-*` name needs a user-level `bmad-*` artifact that step 3.6 forbids, and made it an explicit owner choice (evidence cannot decide) in `synth-04` Section 9 row 2 (sub-question) and row 3 (the (yes, b) combination), plus the Phase 4 branch table, step 3.6, Plan basis and feasibility paragraph.
- Files: `synth-02` section 3.1 reading table and 4.4 Owner Q2 row; `synth-03` Q2 definition, Limits row 1 (new sentence), Section 7 diagram, Table 1 and Table 2 "Which reading" cells, Dependence rows 2 and 3, limit 3; `synth-04` as listed.

## Finding 8 (Section 7 says D-1 and D-2 are decided; Section 8 and Section 9 row 10 leave them open): FIXED

- Re-read `synth-04` step 3.2 condition 2 (bare `[ ! -e "$P/_bmad" ]`), step 3.3 (no atomic step, broken-install message only), step 3.4 (owner has not decided D-10, Variant H is a default) and Section 9 rows 5, 6 and 10 (D-10, D-3, and D-1, D-2, D-6 handed to the owner).
- The finding proposed "D-3 and D-10 decided here"; the evidence shows D-3 (step 3.2 and row 6) and D-10 (step 3.4 and row 5) are also owner-open with a plan default, so all four are worded as plan defaults, not decisions. This is a deliberate, evidence-based deviation from the proposed wording; no decision was invented.
- `synth-03` Stage 0 item (c) now reads "plan defaults, not settled decisions" with the four defaults (D-1 no atomic step; D-2 bare `_bmad/` existence for FIRST_USE; D-3 repo top; D-10 hidden) and the rows that keep them open (9 rows 10, 6, 5).
- `synth-04` step 3.2 condition 2 now says why it stays bare existence (never run the installer over any existing `_bmad/`; a config.toml guard would let a partial tree read as first use and `--yes` over a partial tree takes quick-update with UNVERIFIED effect, R-10, G-13); step 3.3 states there is no atomic step (D-1 default) and that its "too weak" remark is about completeness, not the FIRST_USE guard; Section 9 row 10 lists the three defaults.
- `synth-02` section 4.4 D-1/D-2/D-6 row and F-05 Notes aligned (defaults in Section 8, owner decision in Section 9 row 10).

## Totals

| Item | Count |
|---|---|
| Blocking findings in the input (BLOCKING_COUNT) | 8 |
| Fixes applied (findings 1 to 8) | 8 |
| Findings not fixed | 0 |
| Fixes applied plus findings not fixed | 8 (equals BLOCKING_COUNT) |
| MINOR rows (9 to 31) acted on | 0 |

Files edited: `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps-external.md`, `synthesis/synth-03-options-recommendation.md`, `synthesis/synth-04-plan-questions-evidence.md`, and this log. No research file, product file, or other repository was edited; nothing was staged, committed, pushed or run.

Notes for the orchestrator:

- Finding 2: research file 02 line 280 says orca_retirement "removes exactly those links"; the code (`modules.tf:105`) also `rm -rf`s the shared copy. The research file is read-only and was not edited; the synth text follows the code.
- Finding 8: D-3 and D-10 are worded as plan defaults too (they are owner questions in Section 9 rows 6 and 5), a deliberate deviation from the finding's proposed wording, because the evidence shows they are open.
- Findings 6 and 7 leave two new owner sub-questions in Section 9 row 2 (is a new, separately named command wanted; is a bootstrap name acceptable instead of a literal `/bmad-*` name). Q1 and Q2 stay unanswered.
- Not re-run by me (taken from the findings, UNVERIFIED by me): `ui.js:233-262` quick-update behaviour (also cited in synth-04 step 3.1 from the research files).
- During the run, three tool calls with a mistyped path or a stray replacement were issued and failed with "File does not exist"; none changed any file.

