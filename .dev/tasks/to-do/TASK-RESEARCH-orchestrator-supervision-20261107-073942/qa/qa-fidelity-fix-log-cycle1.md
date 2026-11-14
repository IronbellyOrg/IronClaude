# Fix log: Phase 6 source-document fidelity gate, cycle 1 (second and last fix pass)

- Findings source: `qa/qa-fidelity-consolidated-findings-cycle1.md` (C1-01 to C1-04, all IMPORTANT)
- Target: `RESEARCH-REPORT-orchestrator-mode.md` (only file edited)
- Kept: NB-4 exception record; both [CONTRADICTION] markers and their resolutions
- MINOR notes: not fixed

## Entries

### C1-01 (IMPORTANT) - FIXED

- Sections: 2 (Section C precedence list, rule 1 and rule 4 entries); 3.1 (classification diagram rules 1 and 4; "Policy is a separate dimension" bullet); GQ-02 gap row; GQ-96 accepted-gap row; 7 (precedence diagram); 8.1 step 1.3 (rule 1, GQ-96 sentence, 4a, 4b-contract); 8.1 step 1.8 (4a, GQ-96 and rule 1 fixtures); gap-to-step table GQ-96 row.
- Change: defined "rule 1's condition" once (row settled, brief `report blocked`, or an `/sc:implement` Ruling halt) and applied it everywhere rule 1, 4a, 4b-contract and the GQ-96 sentence are stated. Step 1.3 now says rule 4's contract sub-cases apply only when rule 1 would have applied; a skipped blocked contract gets no class from 4a or 4b-contract and policy "could not determine" with the may-be-re-running note, never "not frozen". 4a counts `blocked_question` only under that condition; 4b-contract freezes on `blocked` only under it. GQ-96 sentence (3.1 bullet, step 1.3, GQ-96 row, gap-to-step row) made conditional. Step 1.8: 4a fixture is on a settled row; GQ-96 fixture is on a settled row or `report blocked`; added the same contract on a live row under `ask the coordinator` (no class from 1/4a/4b-contract, policy could not determine) and a live `E-HALT-QA` contract under `ask the coordinator` (class (a), frozen); the rule-1 ask-the-coordinator fixture also asserts not (a) or frozen under rule 4. Section 7 diagram and GQ-02 row aligned.
- Source-to-source conflict named in the report: Section C rule 1 and 4a (`research-notes.md:192`, `:196`) and GQ-96 (`gaps-and-questions.md:119`) state the rules unconditionally; WC-3 (`WORKER-CONTRACT.md:54-56`) shows a blocked contract under `ask the coordinator` can be replaced by the re-run, and that a Ruling halt is never asked. The report follows WC-3. The freeze rule (`:133`) reads the latest contract, so the skipped case prints policy could not determine, not "not frozen".
- Evidence: Read `src/superclaude/core/WORKER-CONTRACT.md:26-137` (WC-2 `:30` every blocked contract carries `blocked_question`; WC-4 `:32` implement `reason` carries the STOP code when blocked; WC-3 `:53-56`; freeze `:133-136`); `grep -n` on `research/research-notes.md` (rule 1 `:192`, 4a `:196`, 4b `:197`); `gaps-and-questions.md:119`. Post-edit grep for "from rule 1", "blocked contract" and "blocked ... waiting on a person": no unconditional statement left (the remaining step 1.9 case, blocked contract with Orca outcome `failed`, is a settled row and meets the condition).

### C1-02 (IMPORTANT) - FIXED

- Section: 8.2 row formerly labelled "S9 rows 7, 8, 9, 30, 51, 53".
- Change: label is now "S9 rows 8, 9, 30, 51, 53"; dropped "report person-started sessions (G6)" from the owner decisions and added a sentence that G6 / GQ-09 / S9 row 7 is settled by the sources (Section 3.1 G6); "all six" -> "all five"; Blocks column "WC-14 G6 wording and rule id" -> "WC-14 rule id".
- Evidence: grep of the report for GQ-09 shows every other place (`:68`, `:324`, `:443`, `:531`, `:649`, `:1076` §7, `:1216` step 1.0b, `:1324`, 9.1 row 7 `:1525`, 9.2 row 66 `:1596`, 9.5 row 106 `:1660`) already says GQ-09 is settled and five decisions are asked; S9 rows 8, 9, 30, 51, 53 (`:1526`, `:1527`, `:1548`, `:1570`, `:1572`) are GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, the same five step 1.0b names.

### C1-03 (IMPORTANT) - FIXED

- Sections: 8.1 step 1.8 (fixtures), 8.1 step 1.9 (classification and safe-to-close tests), SC-4 row ("How it is checked").
- Change: step 1.8 adds `patch_git` fixtures for `git status --branch --porcelain` (branch with no upstream; branch ahead of upstream) and `git status --porcelain -- .dev/tasks` (untracked path; unstaged path under `.dev/tasks/`), plus a `_git` raising `subprocess.CalledProcessError`. Step 1.9 adds one safe-to-close case per fixture, built through the step 1.4 git probe, each asserting "worktree removable: no" with the condition named, and a failed-git case asserting `unpushed` / `dev_tasks_unsaved` is `None` and "worktree removable: could not determine". SC-4 names these tests.
- Evidence: Read `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:58-70` (`:60` "`.dev/tasks/` content is never classed as disposable"; `:68` mock-based tests for "git cleanliness, unpushed commits, unfinished ledgers"). The git commands and the `unpushed` / `dev_tasks_unsaved` fields are those step 1.3 and step 1.2 already define; `status` is in the step 1.4 git allowlist, so no new probe form is introduced.

### C1-04 (IMPORTANT) - FIXED

- Sections: 8 "Rollback (Phase 1)" rationale paragraph and the "Four registries" row.
- Change: the row now also reverts the step 1.21(b) "Orca coordination" edits (the coordinator-runs-`/sc:sweep` bullet, and `/sc:sweep` removed from the "Some commands are never workers" bullet at `:403`, which step 1.21(b) extends to name it), and says the plugin byte copy is re-copied after both the "Other commands" and the "Orca coordination" reverts (and in the follow-up PR if part (b) moved there, matching step 1.23). The rationale paragraph now says the same "removed command" argument covers those bullets.
- Evidence: report step 1.21 (b) and step 1.23 (read in this pass); `src/superclaude/core/HOW-WE-WORK.md:396` "## Orca coordination" and `:403` "Some commands are never workers" bullet (read via `sed -n`, no edit).

## Summary

- Fixed: 4 (C1-01, C1-02, C1-03, C1-04). Not fixed: 0.
- Only `RESEARCH-REPORT-orchestrator-mode.md` was edited; no source file changed (`git status --short src/` empty). NB-4 record and [CONTRADICTION] markers untouched (`grep -c`: NB-4 23 hits, CONTRADICTION 6 hits, both unchanged areas).

