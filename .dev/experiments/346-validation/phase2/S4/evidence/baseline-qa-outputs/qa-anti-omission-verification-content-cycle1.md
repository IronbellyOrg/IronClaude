# QA Report - Gate 5 Anti-Omission Content Verification (cycle 1, agent 2 of 2)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix authorization:** false

---

## Scope and inputs read

- Consolidated findings (154 lines) read in full: BLOCKING_COUNT 4 = O-5 (row 5), O-8a (row 7), OM-1 (row 65), OM-2 (row 66).
- Fix log cycle 1 (51 lines) read in full: all 4 reported FIXED; Section 9 row 20 added.
- Report `RESEARCH-REPORT-bmad-first-use.md` read in full, lines 1-1805 (10 chunks). Line numbers below are of that file as read in this session.
- Sources re-read read-only: installer `ui.js:795-875`, `ide/_config-driven.js:436-455, 495-520, 780-808`, `ide/shared/installed-skills.js:30-60`, `core/installer.js:90-105, 400-430` (all under `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/`); `research/web-01-...md:120-165`; `templates/VSCode-AIDev02/llm-env.tf:1-45`.

## Check 1: Recovered text accurate against the cited sources

| Row | Claim in the report | Source line read | Result |
|---|---|---|---|
| 5 (O-5) | Any ONE of `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` selects the partial-seed branch (`ui.js:807`) | `ui.js:807` is exactly that four-way OR | ACCURATE |
| 5 | Flagless `--yes` takes the default branch (`ui.js:838`), seeds only when existing core config is empty (`:843`) | `ui.js:838-843` | ACCURATE |
| 5 | Seeds capitalised OS username, `path.basename(directory)`, English, English, `_bmad-output` (`:844-861`) | `ui.js:850` `charAt(0).toUpperCase()`, `:855-858` the four other keys | ACCURATE |
| 5 | `install.sh:42` flag set writes only `user_name` and `output_folder` (`ui.js:807-837`) | `ui.js:809-824` writes only the flags given; `:832-837` no prompt under `--yes` | ACCURATE |
| 7 (O-8a) | Existing `<canonicalId>` skill dir removed before copy (`_config-driven.js:445-448`) | `:446-447` `fs.remove(skillDir)` | ACCURATE |
| 7 | Cleanup removes only the previously installed set plus `removals.txt` (`:499-516`) | `:503-516` | ACCURATE (install flow; uninstall flow uses `_buildUninstallSet`, not claimed) |
| 7 | `bmad-os-*` always preserved (`:789-790`), `isBmadOwnedEntry` false for it (`installed-skills.js:45`) | `:789-790`, `installed-skills.js:45` | ACCURATE |
| 7 | After the IDE step `_cleanupSkillDirs` deletes the skill source copies under `_bmad/<module>/` (`installer.js:97-101, 406-425`) | `installer.js:97-101`, `:406-425` (removes `dirname` of every `skill-manifest.csv` path) | ACCURATE |
| 65 (OM-1) | Ranking remote settings, MDM/OS policy, managed files; default `first-wins`; `ANTHROPIC_BASE_URL` non-Anthropic starts at the next source (web-01:143) | `web-01:143` quoted as stated | ACCURATE as quoted; see finding M-2 (a readable repo fact left "not established") and M-5 (garbled parenthetical) |
| 66 (OM-2) | Frontmatter hooks register on invocation; project skill hooks register "including in a `-p` run in a folder you haven't trusted" (web-01:127, 157); web-01:156 states the absolute sentence | `web-01:127`, `:156`, `:157` | QUOTES ACCURATE; the conclusion drawn from them is NOT supported, see finding I-3 |

## Check 2: Consistency across every occurrence (greps over the report)

| Recovered rule | Search | Result |
|---|---|---|
| FIRST_USE(P) condition 3 reads "other than `bmad-os-*`" | Grep `bmad-\*` (80 lines), read each in predicate context | CONSISTENT at l.292, 529, 578, 612, 651, 1022, 1396, 1465, 1624. Unqualified `bmad-*` at l.1408 is the manual-user wording the fix log left on purpose; l.1339, 1481, 1490, 474, 497 describe state, not the predicate |
| `--output-folder` must stay only where `--user-name` is passed | Grep `output-folder` (-i, 36 lines) | QUALIFIED at l.121, 568, 1021, 1438, 1464. NOT qualified at l.406 ("Every first-use command must keep `--output-folder _bmad-output`"), l.681 (G-14 target cell "kept in every command"), l.910 (W02-6 "stays in every command"). These three contradict the flagless alternative added at l.121, 568, 1464, 1718. Finding I-2 |
| Step 5.3 case (d) `bmad-os-x` fixture | Read l.1542 | The fixture is added, but the sentence "(c), (d), (e) leave P byte-identical" (l.1542, only match) was not updated. Finding I-1 |
| W01-18 wording "no hook-based option escapes it" | Grep `escapes it|no hook` over the task folder | Report l.867 now says "no settings-file hook option escapes it"; l.1526 reworded; the old sentence survives only in `synthesis/synth-02:324`, the research file and the QA files (not report text). No stale copy in the report |
| D2 risk factor R6 | Grep `R6` and `High \(R4, R5\)` | l.1146 (Option D table) lists R4, R5, R6 for D2; l.1236 (Table 1) still reads `High (R4, R5)`; Section 6.0 rubric (l.1013) defines R1 to R5 only; `R6` also names a prior position of research-notes F9-3 at l.1325, 1397, 1669. Finding M-1 |
| Row 20 reaches the recording rules | Grep `rows 5, 6 and 10` / `row 20` | Row 20 is cited at l.121, 292, 298, 568, 674, 1021, 1464, 1465, 1542 but NOT at Stage 0 (c) l.1306, step 1.1 l.1391, Phase 3 header l.1460, "what is not decided" l.1365 or the checklist l.1664, which list rows 5, 6, 10 only. Finding M-3 |
| Inference labels untouched | Grep `synthesis inference:` | 15 bracketed labels at l.438, 574, 741, 986, 1069, 1245, 1307, 1316, 1321, 1351, 1361, 1371, 1480, 1700, 1701, plus the explanatory mention at l.1797; each reads intact. No label was added or removed by the four recoveries |

## Check 3: Placement, options/recommendation/plan, Q1/Q2, Feasibility, scannability, actionability

| Question | Evidence | Result |
|---|---|---|
| Each recovery sits where a reader looks for it | O-5: Section 2.1 flag paragraph (l.121), definition (l.292), step 3.1 (l.1464), Section 9 row 20. O-8a: Section 2.1 created-path rows (l.90, 95), new table (l.294-300), step 3.2 (l.1465), step 5.3 (l.1542), row 20. OM-1: W01-17 (l.860), G-03 (l.670, 974, 1728), Option D step 7 and risk/cons (l.1141, 1146, 1150), Rationale 5 (l.1320), Q-table row 5 (l.1355), step 4D.6 (l.1528), row 15 (l.1713). OM-2: W01-18 (l.867), step 4D.4 (l.1526) | PASS |
| Options, recommendation, plan reflect the recovered facts | OM-1 reaches Sections 6, 7, 8, 9 (above). O-8a and O-5 reach step 3.1, 3.2, 5.3. Defects: I-1 (step 5.3 assertion), M-1 (Table 1 risk cell), M-3 (row 20 not in recording rules) | PARTIAL, see findings |
| Q1 and Q2 intact and unanswered | l.1347 (Section 7), l.1699-1700 (Section 9 rows 1, 2), l.740-741 (4.4) read: wording unchanged, no answer added. Row 20 is new, is labelled "Owner or implementer decision; no answer is invented here", and answers nothing | PASS |
| Feasibility statement intact | l.1327-1343 read: both answers (Yes, Yes), "Stop condition: not triggered", five limits unchanged. Only Rationale row 5 (l.1320) gained a D2 caveat. Section 9 row 4 (l.1702) unchanged | PASS |
| No owner decision invented | Row 20(a) and 20(b) present plan defaults and alternatives; step 3.1 says "does not choose between the two"; step 3.2 says "implementer or owner choice, not decided here" | PASS |
| Scannable (tables, not walls) | O-8a recovery is a 3-row table (good). O-5 was appended to the single paragraph at l.121 (now about 3.5k characters); W01-17 (l.860) and the W01-18 relationship line (l.867) are single run-on blocks of about 1.4k and 1.8k characters while sibling findings use short sub-bullets; step 3.1 and 3.2 cells grew by about 1.2k and 1.5k characters | PARTIAL, note M-4 |
| Recovered plan steps actionable (files, functions, outcomes) | Step 3.1 alternative: exact command, keys seeded, cost (PASS). Step 3.2 condition 3: exact glob rule, fixture (PASS). Step 5.3 (d): fixture named, but the assertion sentence contradicts it (I-1); no step observes which core keys the chosen flag set wrote (M-7). Step 4D.6: caveat only, no new step, appropriate | PARTIAL |
| Stop-and-re-scope branch | Section 7 states a feasible plan and Section 8 starts with "Plan basis", not "RE-SCOPE PROPOSAL"; the normal branch applies | PASS (the re-scope condition is not met, so the recovered items were checked against the normal plan, as above) |

## Issues found

Blocking (IMPORTANT, each needs a fix and a re-check):

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| I-1 | IMPORTANT | Section 8 step 5.3, l.1542 | The O-8a recovery added a `bmad-os-x` fixture to case (d) and says it "is first use" under the plan default, so the install runs and P changes. The same step still asserts "(c), (d), (e) leave P byte-identical". The test as written fails on its own fixture. | Reword to "(c), (e) and the `bmad-x` fixture of (d) leave P byte-identical; the `bmad-os-x` fixture of (d) is asserted as a first use (or as untouched if row 20(b) picks the stricter glob)". |
| I-2 | IMPORTANT | Section 2.5 l.406; Section 4.2 G-14 l.681; Section 5.2 W02-6 l.910 | The O-5 recovery qualified the `--output-folder` rule to "commands that pass `--user-name`" at five places (l.121, 568, 1021, 1438, 1464) but three places still say it is kept in "every first-use command" or "every command". They contradict the flagless alternative (no `--output-folder`) that the same report now presents. | Add "that passes `--user-name`" (or "see Section 9 row 20") at l.406, l.681 and l.910. |
| I-3 | IMPORTANT | Section 5.1 W01-18 relationship, l.867; Section 8 step 4D.4, l.1526 | The OM-2 recovery concludes that a skill-frontmatter hook "is therefore a variant of option B that the hold-back does not gate" and that "no hook option escapes the hold-back would be wrong". The only quote used (web-01:127, 157) is about `-p` runs. The same W01-18 bullet (l.864) and web-01:155 say `-p` and SDK sessions treat every folder as trusted and run settings-file hooks there too, so a `-p` quote cannot show that a frontmatter hook escapes the INTERACTIVE hold-back. web-01:157 speaks of `allowed-tools` and the parent-trust column, not an interactive never-trusted folder. The "therefore" sentence is an unlabelled synthesis inference, and the repo labels its inferences. | Say what the sources say: the docs do not state whether a frontmatter hook runs in an interactive never-trusted folder, and web-01:156 and 127 disagree. Put the variant under `[synthesis inference: ...]` or `[UNVERIFIED - doc-only]` as a candidate only. In step 4D.4 replace "would be wrong" with "not shown either way for the frontmatter case". |

Notes (MINOR, not rechecked):

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| M-1 | MINOR | Section 6 Option D table l.1146 vs Table 1 l.1236; rubric l.1013 | D2 risk is "R4, R5 and R6" in the option table and "High (R4, R5)" in Table 1; the rubric defines R1 to R5 only; `R6` also names a prior position (research-notes) at l.1325, 1397, 1669. The High rating is unchanged. | Define the factor in the rubric under a label that does not collide with research-notes R6, and add it to the Table 1 cell. |
| M-2 | MINOR | W01-17 l.860 and the places that copy it (l.1141, 1146, 1150, 1320, 1355, 1528, 1713, 1728) | "Whether a Coder workspace sets `ANTHROPIC_BASE_URL` was not established (the research did not read a config file for it)". `templates/VSCode-AIDev02/llm-env.tf:24-28` sets `ANTHROPIC_BASE_URL` to the LiteLLM gateway `http://192.168.133.101:4000/cli` for every agent process, and `README.md:264` says so. By web-01:143 a non-Anthropic base URL skips remote settings, which lowers the R6 weight the recovery spread over ten places. Also "authenticates ... through a gateway" paraphrases a truncated quote ("signs in to a gateway ...") and sits next to the base-URL sentence without reconciling them. | Cite `llm-env.tf:24-28`; keep the ranking effect tagged doc-only; keep MDM/OS policy as the open part. |
| M-3 | MINOR | Section 7 Stage 0 (c) l.1306; step 1.1 l.1391; Phase 3 header l.1460; l.1365; checklist l.1664 | The two new open defaults of row 20 (flag set, `bmad-os-*` glob) are not in the recording rules (assumption and question memlog bullets "Section 9 rows 5, 6, 10") or in the list of what waits for owner answers. | Add row 20 to those lists. |
| M-4 | MINOR | l.121; l.860; l.867; step 3.1 and 3.2 cells | Recovered text lengthened already long blocks. | Split into short sub-bullets or a small table (branch, flags, keys seeded). |
| M-5 | MINOR | W01-17 l.860 | "(option D2, and the check for `allowManagedHooksOnly` and `strictPluginOnlyCustomization`) is therefore ignored": it is a drop-in's contents (and the keys in it) that first-wins would ignore; the check of the image's `/etc/claude-code/` is not ignored. The earlier sentence "if a file under `/etc/claude-code/` set either key, B and D would stop working" is not reconciled with first-wins. | Reword. |
| M-6 | MINOR | l.121, 294, 867, 1718 | "audit recovery, O-5 / O-8a / OM-2" and "re-read in this pass" are QA-process labels a reader of the report cannot resolve; the tags `[UNVERIFIED - never run]` and `[UNVERIFIED - derived, not run]` are not in the Section 6.0 tag key. | Drop the process labels or define them; add the tags to the key. |
| M-7 | MINOR | Step 5.3, l.1542 | Neither flag-set alternative has a CI observation of which core keys it wrote (`_bmad/core/config.yaml`), so the row 20(a) choice will have no evidence beyond code reading. | Add "record the keys of `P/_bmad/core/config.yaml`" to case (a). |

## Self-Audit

What I checked, with tools:

- Read in full: the consolidated findings (154 lines), the fix log (51 lines) and the whole report (1805 lines, 10 chunks), so every recovered location was seen in context and not only the places the fix log names.
- Re-read the installer sources the recoveries cite (`ui.js:795-875`, `_config-driven.js:436-455, 495-520, 780-808`, `installed-skills.js:30-60`, `installer.js:90-105, 400-430`): all 8 installer claims of rows 5 and 7 reproduce, so the two installer recoveries are accurate.
- Re-read `web-01:120-165` for rows 65 and 66: the quotes reproduce; the inference drawn in row 66 does not follow (I-3).
- Ran consistency searches over the report for `bmad-*` (80 lines), `output-folder` (36 lines), `every command`, `escapes it|no hook`, `R6`, `High (R4, R5)`, `rows 5, 6 and 10`/`row 20`, `synthesis inference:` and `audit recovery`. These found I-1, I-2, M-1, M-3 and M-6. Searched the repo for `ANTHROPIC_BASE_URL` and read `llm-env.tf`, which found M-2.
- Tool calls: Read 23, Grep 12, Glob 0, Bash 0 (23 + 12 = 35 against 25 check rows in the three tables, above the minimum).

Why the count is credible: three blocking findings and seven notes. I started from the assumption that recoveries contain errors and tried to break each of the four. Two (rows 5 and 7) are accurate at source level but were left inconsistent in the report (I-1, I-2). Row 65 is accurate as quoted but incomplete (M-2, M-5). Row 66 over-reads its source (I-3). A zero count would not have been believable given that the fix log lists only the places it edited and never claims a search for remaining occurrences.

UNVERIFIED by me: I did not run `bmad install` or any test, so the behaviour of the flagless form and of an install beside a `bmad-os-x` skill is a code reading only, as the report says. I did not fetch the Claude Code documentation pages, so the web-01 quotes were verified against the research file, not the live docs. I did not diff the report against its pre-fix state (it is untracked), so "no label added or removed" rests on the label list above and the fix log.

## Verdict: FAIL

- Blocking issues: 3 (I-1 Section 8 step 5.3; I-2 Sections 2.5, 4.2, 5.2; I-3 Section 5.1 W01-18 and Section 8 step 4D.4).
- Severity counts: CRITICAL 0, IMPORTANT 3, MINOR 7 (M-1 to M-7).
- Checks: 4 of 4 recoveries present and placed correctly; 2 accurate at source level (O-5, O-8a), 1 accurate as quoted (OM-1), 1 over-reads its source (OM-2). Q1, Q2, the Feasibility statement and all 15 inference labels are intact.

## QA Complete

