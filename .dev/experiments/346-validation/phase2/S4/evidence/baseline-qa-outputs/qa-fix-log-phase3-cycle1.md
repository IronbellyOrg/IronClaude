# Fix log: Gate 1 (research completeness), fix cycle 1

**Status:** Complete
**Date:** 2026-11-08

---

## Finding 6 (fixed by the fix agent)

- File: `research/01-bmad-6-9-0-installer-and-skill-runtime.md`, section 7.4 row "40 SKILL.md files ... (92 occurrences)".
- Re-verification: Grep `resolve_config|resolve_customization`, path `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/src`, glob `**/SKILL.md`, count mode: "52 total occurrences across 39 files"; `-o` content mode listed 52 matches. Grep `_bmad/(bmm|core)/config\.yaml` gives 37 files (reproduces). Glob of `**/SKILL.md` under `src` lists 46 files (reproduces).
- Change: row replaced with "39 of 46 SKILL.md files (52 matches)" plus the counting method and a correction note.

## Finding 7 (fixed by the fix agent)

- File: `research/01-bmad-6-9-0-installer-and-skill-runtime.md`: new section 3.2a (before 3.3), edits to the 8.1 command row, a new Gaps row U13 (UNVERIFIED count 12 -> 13 in the Gaps header and the Summary).
- Re-verification by Read: `ui.js:775-870` (branch at 807, `else if (options.yes)` at 838, guard at 832-837, defaults at 851-859); `official-modules.js:1023-1046` (core filtered at 1029-1032); `installer.js:949-1037` (core config spread into module configs at 983-989); `manifest-generator.js:468-545` (core keys partitioned by scope); `src/core-skills/module.yaml:8-23` (user_name and communication_language have `scope: user`); `bmad-dev-story/SKILL.md:50-53` reads all four keys with no stated fallback.
- Result: with the `install.sh:42` flags only `user_name` and `output_folder` land (config.toml [core] gets `output_folder`, config.user.toml [core] gets `user_name`); `project_name`, `communication_language`, `document_output_language` land nowhere. Plan facts recorded: keep `--output-folder _bmad-output`; any of the four core flags selects the partial branch, bare `--yes` selects the full-default branch; `--set core.project_name` effect on files is UNVERIFIED (set-overrides.js not read).

## Finding 8 (fixed by the fix agent)

- File: `research/05-startup-boot-test-docs-and-decision-trail.md`: part (d) row d5, part (b) slug-configuration row (line 53), part (b) Key Takeaways, part (d) Key Takeaways, Gaps U6, CODE-CONTRADICTED table (C5 row removed, count 7 -> 6, withdrawal note added, C6/C7 IDs kept), Stale Documentation bullet 5, Summary count.
- Re-verification by Read: `slug-configuration.md:45-57` (line 51 command passes `--user-name`; line 53 is "Mandatory flag ... Without it, 6.9.0 creates a literal `{output_folder}/` directory"); `ui.js:807-837`; `official-modules.js:1362-1415` (`return configValue || match` at 1409).
- Result: re-tagged "mechanism CODE-VERIFIED (official-modules.js:1409), outcome UNVERIFIED (not run)"; the instruction that every first-use command passes `--output-folder _bmad-output` is kept.

## Finding 1, part applied by the fix agent (the 05 blanket correction)

- File: `research/05-startup-boot-test-docs-and-decision-trail.md`: row a-supplement 449-452, both Key Takeaways blocks (a) and (a-supplement), and the Summary.
- Change: "B and D leave every row unchanged / are unaffected" is now limited to the first-use ACTION (after boot) and to the variants that never run through `bmad/install.sh` (B2, B3, D2, D3); B1 and D1 (delivered at boot by install.sh) are stated to break test-57:450 (whole-HOME `snap`, test-57:146-153) and, for D1, `ic_hooks` (test-57:140), per 04 section 7. The reconciled matrix itself comes from the gap researcher addendum (below).

## Finding 3 (fixed through gap researcher; addendum merged in the research file)

- File: `research/02-image-cli-and-catalogue-slug.md`, `## Addendum (fix cycle 1): Sysbox image-layer headroom gate (Finding 3)` (Status Complete, inside the file at line 382 onward).
- Fix agent checks: re-read `coder-ci-aidev02-contract.yml:1016-1029` (gate fails above 70 layers, line 1026); `git -C <worktree> rev-parse HEAD` = `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1`, the same commit as the CI run cited in the addendum.
- Result: current count 68 of 70 (CI log line `Sysbox image layers: 68 (budget: 70)`, run 42346410588 on f1ac0c93 and the newest main run), tagged as read from CI logs. Layer-cost column: B1 0, B2 +1 (0 via fold into an existing COPY), B3 0, C 0 (+1 as a standalone COPY), D1 0, D2 +1 (no fold without editing the test-73 pin), D3 0. Comments reconciled: `Dockerfile.coder:229` ("two spare") matches the measurement, `:468` ("no headroom") is stale as a measurement and holds as policy.
- Deviation from the proposed fix, with reason: the finding proposed marking every +1 option "blocked". The evidence does not support that (68 of 70 leaves two free layers), so the addendum marks B2 and D2 "layer-constrained" instead. The researcher listed its 6 UNVERIFIED items (U15-U20) and 1 CODE-CONTRADICTED item (C8) inside the addendum, not in the existing Gaps section, to keep the append-only rule.

## Finding 9 (fixed through gap researcher; addendum merged in the research file)

- File: `research/research-notes.md`, `## Addendum (fix cycle 1): Finding 9 ...` (Status Complete, line 141 onward).
- Fix agent checks: `BUILD-REQUEST.md:14` contains the decision text ("the user decided"); `REPORT.md` lines 89, 91 and 100 contain "MUST NOT change", "writes nothing" and "DANGEROUS".
- Result: read REPORT.md (141 lines) and all 12 files under `.dev/issues/478/` (one-line relevance each); 16 REPORT.md positions (R1-R16) each marked superseded or still in force; prior "user-scope install UNVERIFIED" answered by 01 sections 2 and 5 (whole-package Grep, 43 hits in one file); one new CODE-CONTRADICTED item (REPORT.md:91 says test-startup-boot pins "no seed: bmad writes nothing", but that assertion exists only in test-57). The addendum records 6 UNVERIFIED and 5 CODE-CONTRADICTED items. No file under `.dev/issues/478/` or `.dev/troubleshoot/` was edited.

## Finding 1 (fixed: 05 blanket correction by the fix agent, plus gap researcher addendum)

- File: `research/05-startup-boot-test-docs-and-decision-trail.md`, `## Addendum (fix cycle 1): Finding 1 - reconciled per-variant matrix (stub delivery vs first-use execution)` (Status Complete, line 294 onward): group 1 "stub delivery" (rows S1-S16c) and group 2 "first-use execution" (rows X1-X6), columns B1, B2, B3, C, D1, D2, D3, E, F, each cell with the assertion file:line or "none".
- Fix agent checks: re-read `test-57-catalogue-configure.sh:138-153` (`ic_hooks` at 140, `snap` at 148-153) and `:444-452` (the "no seed: bmad writes nothing" check at 450); Grep of test-57 for `startup.sh|seed_if_absent|modules.tf|aidev-startup|SessionStart` returns 0 matches; re-read `test-startup-boot.sh:615-639` and `:2629-2638` (the lines cited for B3/D3).
- Result: the only certain break is `test-57:450` for B1, D1 (and E, F when run from install.sh at boot); B2, B3, C, D2, D3 have no certain break, only BREAKS-IF conditions on static or live-boot pins. File 04 meant B1/D1 by "B" and "D"; file 05 meant the first-use action. 05's blanket wording was corrected in four places and the Summary; after the researcher reported that the Summary wording still named "C" (its C-F1-2), the fix agent corrected that sentence to B1, D1, E, F. The addendum's 6 UNVERIFIED and 3 CODE-CONTRADICTED items are merged into 05's Gaps section as a table ("Fix cycle 1 additions from the finding 1 addendum").

## Finding 2 (fixed through gap researcher; addendum merged in the research file)

- File: `research/04-pinned-tests-57-46-19.md`, `## Addendum (fix cycle 1): Finding 2 - pinned-test inventory ...` (Status Complete, line 269 onward, sections A.1-A.11 plus "Addendum Gaps and Questions").
- Fix agent checks: `test-1-catalogue-shape.sh:25` (`EXPECTED_JOINED="install.sh manifest.yaml module.tf"`), `test-73-claude-retention.sh:23, 100-119` (`copy_ok`, `REL`) confirmed by Grep.
- Result: all 30 files of the `startup.sh|Dockerfile.coder|aidev-startup` search (141 hits) listed and classified (15 relevant, 15 irrelevant, with reasons); the nine tests named in the finding that are not among the 30 are covered separately; per-variant "breaks / does not break" with file:line; proposed assertion text per variant (A.11). The researcher noted that sections A.4-A.6 are slightly out of order (an append slip, labelled in the file). 8 UNVERIFIED and 1 CODE-CONTRADICTED item are listed in the addendum; a pointer was added to the Gaps sections of 02, 03 and 04.

## Finding 4 (fixed through gap researcher; addendum merged in the research file)

- File: `research/03-startup-flow-home-and-user-level-claude.md`, `## Addendum (fix cycle 1): Finding 4 first-use trigger predicate, per-option walkthrough, block-bare-python.sh (01 U8)` (Status Complete, line 238 onward).
- Fix agent checks: Grep `python3 ` over `**/SKILL.md` in the 6.9.0 package gives 41 matches in 31 files (reproduces); `block-bare-python.sh` Grep confirms the command-word check for `python3` (line 134 area).
- Result: one predicate `FIRST_USE(P)` (repo top, `_bmad` absent, no on-disk `.claude/skills/bmad-*`, writable) tied to the guard at `catalogue/bmad/install.sh:24` (and the no-`.git` branch at :22); a walkthrough per option; 01 U8 closed (hook packaged at `install_hooks.py:85`, exits 2 on `python3`, reaches Default-profile workspaces through the ironclaude slug); consequence stated: the 41 `python3` skill steps are blocked there and the written fallback exists in 25 of 31 files (6 have none); corrections to 01 section 7.5 noted in the addendum. U7 and U9 are stated to stay open until web-01. The addendum lists 12 UNVERIFIED items; a pointer was added to 03's and 01's Gaps sections.

## Finding 5 (fixed through gap researcher; addendum merged in the research file)

- File: `research/01-bmad-6-9-0-installer-and-skill-runtime.md`, `## Addendum (fix cycle 1): Finding 5 prior-review observation (memlog), CI test-57 evidence, version-skew risk` (Status Complete, line 388 onward).
- Fix agent checks: re-ran read-only `gh run view 42384399575 --repo IronbellyOrg/Coder --log` filtered for `cold bmad:`: log line `cold bmad: 374 ms` confirmed.
- Result: memlog lines 20, 21, 81 quoted exactly and tagged "prior-review observation, not re-run"; the "about 4 s" is shown to include an npx fetch (not the baked CLI), CI shows 374-392 ms for the whole baked `install.sh` with `--network=none` (test-57:64-66; workflow:1241); U1, U10, U11, U12 narrowed with replacement wording; "6.9.0 over an existing 6.10.0 or partial tree" risk rows added for B, C and D tied to `FIRST_USE(P)`; the `{output_folder}` defect is quoted as the `--user-name` combination, not as a bare-`--yes` defect. 12 UNVERIFIED and 3 stale or CODE-CONTRADICTED items listed in F5-G.

---

## Totals

- Blocking findings in the input: 9 (numbers 1 to 9).
- Fixes applied: 9 (findings 1, 2, 3, 4, 5, 6, 7, 8, 9).
- Findings not fixed: 0.
- Fixes applied + not fixed = 9 = BLOCKING_COUNT.
- Note on finding 3: the proposed fix said to mark any option needing a new layer as blocked; the measured count (68 of 70) does not support that, so B2 and D2 are marked layer-constrained with the reason recorded in the addendum. All remaining open points are tagged UNVERIFIED in the addenda and Gaps sections (for example U7/U9 until web-01).
- MINOR findings 10 to 18: not acted on (no cross-reference notes, no count or line corrections for them were made).
- Gap researchers spawned: 6 (rf-task-researcher, one per gap: findings 1, 2, 3, 4, 5, 9), each on a different target file (05, 04, 02, 03, 01, research-notes.md). All six wrote their addendum inside the target file (none used the `.addendum.json` or inline fallback). No product code, no `.dev/issues/478/` or `.dev/troubleshoot/` file was edited; no `bmad` command was run by the fix agent; nothing was staged or committed.

**Status:** Complete
