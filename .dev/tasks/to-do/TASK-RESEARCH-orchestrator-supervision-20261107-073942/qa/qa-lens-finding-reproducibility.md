## Finding-Reproducibility QA Report

**Report under review:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**QA phase:** report-lens-finding-reproducibility (one dimension only)
**Date:** 2026-11-07
**Fix authorization:** false (report only; no file other than this one was edited)

_Status: complete. Report read in full (lines 1-1651, 150-line chunks); about 55 citations re-read against source._

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT (blocking) | 8 Integration Checklist `:1166`; also `:415`, `:529`, `:616`, `:1340`, `:1449`, `:1570` | `:1166` says `WORKER-CONTRACT.md` holds "WC-1 to WC-13; no WC-14 today" and tags it [CODE-VERIFIED]. It cannot be reproduced: the rules in `src/superclaude/core/WORKER-CONTRACT.md` are WC-2 to WC-13, and a grep for `WC-1\b` over `src/superclaude/core` finds nothing. The research files say so too: `research-notes.md:114` ("WC-1 is unused"), `qa-research-evidence-report-1.md:30` ("no WC-1"). GQ-11 is then posed against a rule that does not exist: `:1340` "amending WC-1" and `:1449` "word WC-14 so it does not override WC-1". | At `:1166` write "WC-2 to WC-13 (WC-1 unused; no WC-14 today)". Restate GQ-11 at `:415`, `:1340` and `:1449` as "add WC-14, or reuse the unused WC-1 ID". Drop "override WC-1". Fix the other mentions to match. |
| 2 | IMPORTANT (blocking) | 8.4 X-1 `:1373` | X-1 says crash-recovery "runs `git stash` commands beyond `list`". The cited evidence does not show that. `sc-crash-recovery/SKILL.md:4` only **permits** `Bash(git stash *)`, and no step of the skill runs a stash command (read `SKILL.md:1-157`). The same contradiction at `:1059` is stated correctly ("`Bash(git stash *)` is allowed"). So the two X-1 rows disagree, and `:1373` is a claim nobody can reproduce. | Change `:1373` to "is described as read-only, but its allowed-tools permit `git stash *` (`SKILL.md:4`)". Do not say it runs stash commands. |
| 3 | IMPORTANT (blocking) | 8.4 X-4 `:1376` vs 4.x X-4 `:1062` | The report gives two versions of the null-`agentWait` resolution. `:1062` calls it "Open" and says "the guide's reading is the safer one". Its rule: null "is valid input for working but never stall proof". `:1376` says "Follow the help reading: null = no wait observed". From these rows a reader cannot tell which reading step 1.3 and its tests implement. The two readings differ on whether null can count toward a stall. | Use one wording in both rows, the `:1062` split rule (null: valid for working, never stall proof; absent: could not determine). At `:1376` replace "Follow the help reading" with "Apply the split rule (guide reading for stop decisions)". Cite `06-orca-open-questions.md` Gap 19 `:144` in both rows. |
| 4 | MINOR | 2.2, 2.4, 3.1, 4.4, 4.6, K-5, `:1229`, `:1311` | The Orca handler files (`message-check-handler.js`, `task-handlers.js`, `run-handlers.js`, `gate-handlers.js`) are cited by file name only. Their directory, `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/`, appears only in the Evidence Trail (`:1622`). The line numbers are correct; I re-read `message-check-handler.js` at `:17`, `:18-19`, `:30`, `:33-34`, `:38`, `:55`, `:58-71`, `:74` and `:82-83`. | Give the full directory once in 2.2, or add a legend line, and say which Orca build it comes from (1.4.245-aidev02). |
| 5 | MINOR | Throughout | Short names are used with no legend: `scope-03:99`, `06:158-175`, `05:163`, `gaps:55`, `[H:worker-show]:16`, `[H:check]:37`, `pragmatic.md:22`, `canvas.py:73-77`, `agent_focus.py:46`, `launch-job-identity.sh`, `analyze-worker-contract.md`, `seed-brief.md`. The memory note `coordinator-never-stop-polling.md` is cited without its path (`~/.claude/projects/-home-coder-workspaces-IronClaude/memory/`). The reader has to search to find these files. | Add a short-name legend near the top of section 10 that maps each short name to its full path. |
| 6 | MINOR | 2.x / 3.1 / 9 (GQ-41) | The command-output citations (for example "`orca-ide orchestration worker-list --help` lines 3, 19-22") do not record the CLI version or where the capture is stored. Another investigator could get different lines from a different Orca build. | For each capture, give the exact command, the Orca version and the stored capture file. |
| 7 | MINOR | Several | The same source is cited with different ranges: HOW-WE-WORK `:314-337` (`:1075`) vs `:318-337` (`:433`); scope-04 skeleton `:268-308` / `:268-304` / `:268-351`; research-notes Section C `:188-204` / `:190-202` / `:188-200` / `:194`; run-handlers `:28-48` / `:35-48` / `:28-34`; crash-recovery 72 h at `:25-27` (`:456`) vs `:26`; ccsession `:558-605` (`:285`) vs `:564-605`. Each range covers the claim, but the differences make readers recheck. | Pick one canonical range for each source and use it everywhere. |
| 8 | MINOR | 4.x A1 reuse row `:961` | `SKILL.md:91,93-97,:120-125,:139-150` puts `:120-125` under `SKILL.md`. At `SKILL.md:120-125` is the pipeline-resume and output-style text. The conflicts section is at `refs/report-template.md:120-125`, which `:146` cites correctly. `:1014` names `report-template.md` without `refs/`. | Move `:120-125` to `refs/report-template.md:120-125` at `:961`. Use `refs/report-template.md` at `:1014`. |
| 9 | MINOR | 2.x `:156`, `:582`, `:1004`, `:1059` | "Pure read-only, enforced by allowed-tools" is quoted from `SKILL.md:13` and `:155`. Only `:155` says it ("Pure read-only — enforced by `allowed-tools`."). `:13` reads "The output is read-only diagnosis. The `allowed-tools` field enforces this". The finding still holds. | Quote `:155` as the source of the phrase and call `:13` a paraphrase. |
| 10 | MINOR | 2.x `:160`; `:456`, `:509`, `:1006`, `:1455` | "`:136` escapes only partly". `bootstrap_scan.sh:136` does no escaping at all (the awk join for `recent_sessions`). The partial escaping is at `:80` and `:107`, and the path itself goes into the JSON unescaped at `:145-146`. The bug is real, but `:136` alone does not show the "partly" claim. | Cite `:136-141` and `:145-146` (no escaping) and `:80`, `:107` (partial escaping). |
| 11 | MINOR | 2.x / 4.x / 8.x | WC-4 is cited as `WORKER-CONTRACT.md:30-38`, but `:30` is WC-2 (`blocked_question`) and WC-4 starts at `:31`. The file is called "203-line", but Read shows 204 lines. The other line numbers in that file were checked and are correct: `:23`, `:45`, `:58`, `:60`, `:74`, `:107-108`, `:126-136`, `:156`, `:158`. | Use `:31-38` and 204 lines. |
| 12 | MINOR | Step 1.21 `:1214`; row `:1450` | Step 1.21 cites "test `:342-347`" with no file name. Row `:1450` shortens `test_never_as_worker_list_names_all_seven_commands` (`test_worker_contract.py:545`) to "all_seven". | Name the test file at `:1214`. Spell the full test name at `:1450`. |
| 13 | MINOR | 2.x, 10 | Counts are given with no command to reproduce them: "allowed-tools set in 14 of 46 command files", "20 headings", "1202 lines", "1975 lines", "41 test functions", "qa/ (24 files)". I did confirm `SKILL.md` 157 lines and `bootstrap_scan.sh` 170 lines by Read. | Give the command for each count, for example `grep -l '^allowed-tools' src/superclaude/commands/*.md \| wc -l`. |
| 14 | MINOR | 2.6 diagram vs 3.1 table vs step 1.4 | The data flows do not match. The 2.6 diagram leaves out `worker-read`, the git reads and `worktree ps`, which the 3.1 table includes. The A1 diagram has `git stash list`, but 3.1 lists git as status/log/branch/rev-parse only. Step 1.4 has all five forms. | Make the 2.6 diagram and the 3.1 table match step 1.4: the full argv list, including `stash list`. |
| 15 | MINOR | 10 Evidence Trail `:1639-1640` | The synthesis list says "synth-05 planned; not yet written" and "synth-06 (this file)". Both are stale. The assembler note at `:1642` corrects them, so a reader has to read past the list to get the right status. | Correct the two lines in place and keep `:1642` as the history note. |

### Markers judged under this lens (not removed)

- **[CONTRADICTION] at `:1078`** (HOW-WE-WORK `:314-337` vs `:318-337`): this is a valid marker, and both ranges can be checked. I re-read the file: `:314` is the `## Other commands` heading, `:318` is `<!-- other-commands:v1 -->` and `:337` is `<!-- /other-commands -->`. One range includes the heading and the other covers only the marker block. A reader can find the claim with either range, so this is a citation-precision note (row 7), not a false claim.
- **[CONTRADICTION] at `:1507-1509`** (allowed-tools colon form `Bash(superclaude sweep:*)` at `:1461`/`:1507` vs space form `Bash(superclaude sweep *)` at `:329`/`:1198`/`:1508`): this is a valid marker, and it is still unresolved in the report. The evidence the report already cites can settle it. `sc-swarm-wizard-protocol/SKILL.md:7` (named at `:961` and in step 1.15) uses the space form `Bash(uv run superclaude swarm *)`. The marker should cite this precedent so the resolution can be reproduced. Recorded as a note; deciding the form is outside this lens.
- **NB-4 exception record** (`:13`, `:206`, `:222`, `:542`, `:1583`, `:1651`): it can be reproduced. `qa/qa-nb4-fix-log.md` exists. It records three edits (`:45`: 2 at `scope-03:99`, 1 at `gaps-and-questions.md:26`) and "all 8 cited lines agree", which matches "three edits... eight dependent lines" at `:1651`. The bare-verb note cited as `qa-nb4-fix-log.md:41` is at `:41`. The log's own out-of-scope note (`:39`) says `gaps-and-questions.md:125` still read 76/24. That line now reads "Open: 75. Resolved: 25", so the later update the report describes at `:222` and `:542` did happen. Verified.

### Summary

- Findings: **18 total**: CRITICAL 0, IMPORTANT 3 (blocking: rows 1-3), MINOR 15 (rows 4-15, plus 3 marker and record notes).
- Checklist (a) reproduce findings from evidence: about 55 citations re-read (well above the 10 required). Rows 1 and 2 could not be reproduced and are blocking.
- Checklist (b) paths and lines locate claims without searching: mostly yes. Exceptions are in rows 4, 5, 6, 8, 12.
- Checklist (c) data-flow traces are complete: the diagrams and tables are each complete on their own but differ from one another (row 14). Row 3 leaves the classifier input rule ambiguous.
- Checklist (d) key patterns are named precisely: the test names, constants and functions I checked are exact (`_POST_REFRESH_ADDITIONS` at `test_routing_refresh.py:33`, asserted at `:648`; `ensure_names_migrated` at `ccsession:285`; `NEVER_AS_WORKER` at `:245-254`; `_check_never_as_worker` at `:398`; `WRITE_VERB_RE` at `:1098`). The exceptions are the nonexistent rule ID WC-1 (row 1) and the shortened test name (row 12).

**Verdict: FAIL** (3 blocking IMPORTANT findings; 15 minor notes do not affect the verdict.)

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist items a-d, each backed by tool evidence; FAIL is due to the blocking findings, not to confidence).

**Tool engagement:**
- After compaction: Read 9 | Grep 6 | Glob 1 | Bash 0.
- Before compaction: about 11 Reads to read the report in 150-line chunks, plus about 15 source Reads and about 10 Greps. These are approximate: the exact counts were not kept across context compaction.

## Self-Audit

**(a) Reliance list (items accepted without my own re-check):**
- No `## Inherited Structural Verdict` was supplied, so I relied on no rf-qa PASS items. Checks were made standalone.
- I relied on the report's own section and line layout (`:390-395` is a fenced mock output, as the brief stated) and did not treat those lines as headers.
- I relied on the earlier QA files only to locate evidence, never as proof. For example, `qa-research-evidence-report-1.md:30` was used to find the WC-1 discrepancy, which I then confirmed in source.

**(b) Independent semantic checks (my own tool work):**
- WC-1 existence: grep for `WC-1\b` over `src/superclaude/core` found no match, and a Read of `WORKER-CONTRACT.md` shows WC-2 to WC-13. This contradicts the [CODE-VERIFIED] tag at `:1166` (row 1).
- crash-recovery behaviour: a Read of `sc-crash-recovery/SKILL.md:1-157` found no step that runs `git stash`; `:4` only permits it, and `:155` holds the "Pure read-only" phrase. This led to rows 2 and 9.
- `bootstrap_scan.sh` (Read `:1-170`): `:31` encodes only `/`, `:73` tests `-d .git`, `:136` does no escaping at all. Confirms the bugs and leads to row 10.
- Attribution of `:120-125`: Read `refs/report-template.md:115-130` shows `## Conflicts and ambiguities` at `:120`, so the `SKILL.md` attribution at `:961` is wrong (row 8).
- allowed-tools precedent: grep shows `sc-swarm-wizard-protocol/SKILL.md:7` uses the space form `Bash(uv run superclaude swarm *)`. This is the evidence relevant to the `:1507` marker.
- Count arithmetic: `gaps-and-questions.md:125` "100 rows, Open 75, Resolved 25" adds up (75+25=100). Checked against the NB-4 log `:39` (76/24 before the fix), so the change is the one GQ-03 row.

## QA Complete
