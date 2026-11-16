# Ponytail review: design docs and gates around the Orca observer (issue 409)

Date: 2026-11-16. Branch 409-Phase2. Read-only review; nothing was edited, moved or deleted except this file.
Root for every path below unless a full path is given: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409 (shortened to B409 only in the Measurements table).
Method: measured sizes, read the live text of the files named in the brief, then grepped code (src/superclaude/cli/observe, tests/observe) and docs for references. Anything not read or run is marked UNVERIFIED.

## Summary

1. Only three pieces of this paperwork are enforced by code or by a test: the gate constant `QUESTION_GATE_PASSED` plus its owner-record file check, the on-screen disclosure strings, and the acceptance test ids (52 of 56 are cited by tests). Everything else is history or copies.
2. The same decisions are written 5 to 10 times across the spec, PRD, risks file and handoffs, and the copies have drifted: the PRD, SPEC.md and the register still say "R0 only, QUESTION-OBSERVATION not passed" while R1 and R2 are built, registered in the CLI and the gate record exists.
3. About 1.5 MB of the 2.0 MB bmad folder (review rounds, extracts, validation reports, a byte-identical second ARCHITECTURE-SPINE.md) and about 600 KB of the brainstorm (debate rounds, a byte-identical merged-output.md) are read by no code, test or live doc; archive them after a reference search and the owner's approval.

## Measurements

Whole folder: B409 = 21 MB on disk (`du`). 136 files are tracked by git under B409. The brainstorm package is untracked (0 tracked files), so a delete there cannot be undone from git.

| Item | Size | Files | Lines (md, yaml, json) | Tracked |
|---|---|---|---|---|
| B409/orca-observer-design-package.zip | 14 MB | 1 | n/a (binary; contents UNVERIFIED, no `unzip` on this host) | listed in README only |
| B409/attachments (22 PNG) | 4.3 MB | 22 | n/a (binary) | yes |
| B409/bmad (all) | about 2.0 MB | 99 | about 13,800 | yes |
| B409/bmad/final-review | 660 KB | 36 | 5,197 | yes |
| B409/bmad/ux-orca-observer | 416 KB | 13 | 2,764 | yes |
| B409/bmad/ux-orca-observer-r2-review | 272 KB | 8 | 1,562 | yes |
| B409/bmad/prd-orca-observer | 260 KB | 15 | 1,761 | yes |
| B409/bmad/architecture-orca-observer | 208 KB | 10 | 1,261 | yes |
| B409/bmad/spec-orca-observer | 196 KB | 12 | 1,109 | yes |
| B409/bmad/handoff-step1..5.md | 17 KB | 5 | 138 | yes |
| B409/tuibbs-review | 132 KB | 9 | UNVERIFIED | no |
| B409/owner-decisions-20261108, 20261111, 20261112, owner-pass-record-20261112 | 6 KB | 4 | 60 | 3 of 4 (20261108 is untracked) |
| /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp | 760 KB | 28 | 4,850 | no |
| Code that these docs describe: src/superclaude/cli/observe | n/a | 21 py/json plus 16 fixtures | n/a | yes |
| tests/observe | n/a | 29 py | 9,639 lines, 402 test functions | yes |

Largest single files (bytes): brainstorm merged-requirements.md and adversarial/merged-output.md 78,427 each; ux-orca-observer/EXPERIENCE.md 77,618; prd.md 59,043; spec ARCHITECTURE-SPINE.md and architecture ARCHITECTURE-SPINE.md 54,129 each; ux-orca-observer-r2-review/validation-report.html 94,437.

Related folders outside B409, measured only: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106 is 52 MB (the README calls it the canonical package, so the 14 MB zip is a copy); the two finished plan folders /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/done/TASK-WF-buildRelease1OfT-20261111-164757 and TASK-WF-release2OfTheOrc-20261111-203306 are about 1 MB each.


## Keep

All paths under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409 unless stated.

| File | Why it earns its place (evidence) |
|---|---|
| owner-pass-record-20261112.md (676 bytes) | Code cites it: src/superclaude/cli/observe/commands.py:67 (`QUESTION_GATE_PASSED = True  # owner record: ...`), and tests/observe/test_commands.py:741-750 fails if the guard is True and the cited file is missing. The only doc that a test reads. |
| owner-decisions-20261108.md, owner-decisions-20261111.md | The only record of decisions 1 to 5 (2026-11-08) and of decisions 6 and 8 plus the own-Run measurement (2026-11-11). Cited by the spec, PRD and release-gates. Short (17 lines each). Note 20261108 is untracked in git. |
| bmad/spec-orca-observer/release-gates.md (13 KB) | The one file kept current (QUESTION-OBSERVATION line 38 records the pass). Holds the data-gate rule that tests/observe/test_golden_contract.py and the golden-*.json fixtures enforce, and the fallback rule. |
| bmad/spec-orca-observer/acceptance-tests.md (14.5 KB) | 52 of 56 ids T1 to T56 are cited by name in tests/observe docstrings and test names (grep of `\bT[0-9]+\b`). It is the traceability table the test files point to. The four ids with no citation are in the Gates section. |
| bmad/spec-orca-observer/adapter-contract.md (12 KB), rendering-rules.md (21.7 KB) | Cited by code docstrings: src/superclaude/cli/observe/questions.py:1 and view.py:197 name them. rendering-rules.md owns the on-screen strings; the disclosure label sits at src/superclaude/cli/observe/view.py:55 and is pinned by 4 test hits. |
| the disclosure label and its sibling strings (`bounded best effort; coverage unknown; ...`, `worker-reported, not questions` (51 test hits), `not proof none exist` (18 test hits)) | Safety and honesty rules that show on screen. Keep the strings and the rules that name them. |
| bmad/spec-orca-observer/snapshot-export-schema.md (8.5 KB) | Backed by src/superclaude/cli/observe/snapshot.schema.json and tests/observe/test_snapshot_schema.py. Keep, but see the merge note: the JSON schema is the enforceable copy. |
| bmad/spec-orca-observer/write-back-future-stage.md (5 KB) | Only record of the write-back threat list and the boundary change. No code reads it, which is correct for a future stage; it is the single source for decision 3. |
| live-test-guide.md (103 lines) | Human run sheet with PASS lines for PR #503; the only human-run check of the live adapter. Whether the owner ran it is UNVERIFIED. |
| bmad/prd-orca-observer/prd.md (59 KB) | The only requirements document in product form. Keep as is after the stale-status edits in the trim list. |
| bmad/spec-orca-observer/unverified-register.md (9 KB), trimmed | 17 of 25 rows in its UNVERIFIED table tie to an on-screen label, a forbidden argv or a test (T5, T18, T21, T51, T52, T53, T54). Keep those; the other 8 are in the trim list. |

## Single source of truth per decision

"Copies" = other live files (not the review and extract folders, not the handoff history) that restate the decision. "Drifted" = a copy whose text is contradicted by a later record or by the repo state. Counts come from grep over the live docs plus reading the lines; wording variants mean the counts are lower bounds.

| Decision | Authoritative file | Copies | Copies that drifted |
|---|---|---|---|
| 1. Staged releases (A first, B after QUESTION-OBSERVATION, C behind QUESTION-LINK), 2026-11-08 | owner-decisions-20261108.md item 1 | at least 8: SPEC.md, owner-decisions-and-risks.md:9, release-gates.md, prd.md (2), handoff-step1, handoff-step2, final-review/owner-decision-pack.md, handoff-mvp-brainstorm.md | 0 on the staging itself. The consequence text drifted, see next row. |
| 1a. DIRECTION-SELECTED status ("not passed, only offline R0 work allowed") | none: no owner-written selection record exists (handoff-mvp-brainstorm.md:35; release-gates.md:10) | 7 live files: prd.md:25, 84, 104, 464; SPEC.md:74; owner-decisions-and-risks.md:17, 66; release-gates.md:10; handoff-step2.md:6; handoff-mvp-brainstorm.md:35, 71; owner-decision-pack.md:144 | All of them as a consequence: R1 shipped (git 9e2608b03, PR #503), `superclaude observe` is registered (tests/observe/test_registration.py), R2 shipped. The recorded basis was a chat authorization, per the reflect assumption A-002 in .dev/reflect/pre-buildRelease1OfT-20261110050109/adversarial/diff-analysis.md:60 (I did not re-read the plan text it cites). prd.md:104 marks R1 "Closed" and SPEC.md:74 says R0 only. |
| 2. Stack: Python + Rich with snapshot export, 2026-11-08 | owner-decisions-20261108.md item 5 | about 9: SPEC.md, owner-decisions-and-risks.md:10, snapshot-export-schema.md, stack.md, prd.md (2), handoff-step1, handoff-step2, handoff-mvp-brainstorm.md (2), tuibbs-review/summary.md (2) | 1 numbering drift: the spec calls it "owner decision 2", the owner file has it as item 5 (prd.md:452 already lists this as OI-11). |
| 3. Write-back is a future stage | owner-decisions-20261108.md item 3 plus write-back-future-stage.md | 17 files mention it; prd.md 16 times, owner-decision-pack.md 14, each EXPERIENCE.md 9 | 0 found. Volume is the problem, not drift. |
| 4. TUIBBS is background only, no AGPL code | owner-decisions-20261108.md item 4 | about 10 (SPEC, risks, stack, schema, prd 3, both EXPERIENCE, REPORT, pack, tuibbs summary 3) | 0 found |
| 5. What counts as a question: "coordinator questions only", 2026-11-11 (decision 8) | owner-decisions-20261111.md | 5 correct copies: SPEC.md, release-gates.md, unverified-register.md, prd.md OQ-7, 12.3 item 8, U4 | 2 stale: bmad/spec-orca-observer/owner-decisions-and-risks.md:24 still lists it as open with a recommendation; SPEC.md Open Questions still lists "What identifies a human question (open owner decision 8)?"; SPEC.md CAP-11 still says "open human question" although the owner decision says the list is never labelled human. |
| 6. Permission to read one named Run, 2026-11-11 (decision 6) | owner-decisions-20261111.md | at least 4: release-gates.md, unverified-register.md, prd.md OQ-5 and 12.3 item 6, owner-decisions-and-risks.md:22 | 3 likely stale: owner-decisions-and-risks.md:22, prd.md:423 and :469, SPEC.md open list still say the permission is open. (The spec's decision 6 is worded as "sample capture and acquisition permission"; the owner's reply is worded as "permission to read that scope". Whether these are the same decision is the orchestrator's call.) |
| 7. QUESTION-OBSERVATION passed, 2026-11-12 | owner-pass-record-20261112.md (owner-written) | 3: release-gates.md line 38, owner-decisions-20261112.md (executor-typed twin, 14 lines), the code comment at commands.py:67 | 3 contradicted: prd.md:106 (R2 gate "NOT passed"), prd.md:491 (U3 "Gate stays closed (NOT passed)"), unverified-register.md:27 ("QUESTION-OBSERVATION: not passed"). handoff-mvp-brainstorm.md:72 says the same but is a dated handoff. |
| 8. Q-1 FAIL (an unbound terminal cannot read) | release-gates.md, proof (b) bullet | 15 files mention Q-1 or consumer_fenced; ux-orca-observer/EXPERIENCE.md alone has 39 hits, ux-orca-observer-r2-review/EXPERIENCE.md 20, prd.md 23 | not checked line by line; UNVERIFIED |
| 9. The 15 spec open questions (OQ-1 to OQ-15) | SPEC.md "Open Questions" (15 lines) | prd.md 12.1 (carried "verbatim"), and the first 10 of them again in owner-decisions-and-risks.md "Open owner decisions" and prd.md 12.3 | the three-way copy has already diverged on items 6 and 8 (rows 5 and 6 above). |

Reading of the table: only the 4 owner records are real sources. The spec, PRD, handoffs and UX files restate decisions in prose, so any new owner record must be hand-copied into up to 8 files, and the last two records (2026-11-11 and 2026-11-12) were copied into release-gates.md only.


## Trim or merge candidates (ranked by reading cost saved)

Nothing was deleted. This repo requires the owner's explicit approval and a reference search before any delete or move; the searches below are the reference searches, redo them at the time of the action. "Archive" means move to a dated folder, never delete first. Paths are under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev unless full.

| Rank | Candidate | Size | Who reads it (grep of src, tests, live docs) | Risk of archiving |
|---|---|---|---|---|
| 1 | Replace the three-way copy of open and decided owner questions with one list. Sources: issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md "Open owner decisions" 1 to 10 (copy), issues/409/bmad/prd-orca-observer/prd.md section 12.1 and 12.3 (about 60 lines, lines 415 to 473; 12.1 "carried verbatim" from SPEC.md, 12.3 restates owner-decisions-and-risks.md), SPEC.md "Open Questions" (15 lines). Keep SPEC.md as the single list; make the other two a link; correct the 5 stale rows from the table above in the same edit. | about 12 KB of repeated text, plus the 5 contradicted statements | Nothing in src or tests. prd.md and SPEC.md cite owner-decisions-and-risks.md by name. | Low. An edit, not a delete. Risk is losing the recommendations text; keep it in one place. |
| 2 | Stale status sweep: prd.md:25, 84, 104, 106, 464, 491; SPEC.md:74; unverified-register.md:27; owner-decisions-and-risks.md:9, 17, 66; handoff-mvp-brainstorm.md:35, 71, 72. Replace "R0 only / NOT passed" with a one-line status that points to release-gates.md lines 10 and 38 and says R1 and R2 are built. | 14 lines | Same files. A reader following prd.md today gets the wrong answer on what may be built. | Low, but needs the owner's word on DIRECTION-SELECTED first (see Gates). Do not write the owner's selection record for them. |
| 3 | Archive the step-5 review rounds: issues/409/bmad/final-review/raw (192 KB), graded (180 KB), verify (60 KB), fixes (52 KB), the three briefs, progress.md, workflow-input.md, inputs (16 KB). Keep REPORT.md and findings.md (88 KB, 160 minor notes) or archive findings.md too. | about 560 KB across 30 files | No code, test or live doc (grep of spec, PRD, README, live-test-guide, src, tests found no path reference; hits for the word "final-review" in src/superclaude/commands/implement.md and the implement skill are an unrelated term). handoff-step5.md and progress.md point at it. | Low for reading. These are the audit trail of 55 blocking findings and 63 fixes (REPORT.md); the git history keeps them because the folder is tracked. Archive, do not delete. |
| 4 | Brainstorm adversarial rounds: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/adversarial (3 rounds of debate, 3 variants, diff-analysis, base-selection, merge-log, refactor-plan, invariant-probe) plus enrichment. Delete the byte-identical duplicate merged-output.md first (78,427 bytes, `cmp` shows it equals merged-requirements.md). | about 600 KB of 760 KB; the duplicate alone 78 KB | merged-requirements.md is cited by prd.md and the prd extracts; merged-output.md only by handoff-mvp-brainstorm.md and the brainstorm's own merge-log and return-contract. The debate rounds are cited only inside the folder. The brainstorm folder is cited as a source pointer by SPEC.md, owner-decisions-20261108.md, tuibbs-review/assumptions.md and the finished plan folders. | Medium: the folder is untracked in git, so there is no copy to recover from. Copy it to an archive location first. Dissent records (INV-007 accepted risk, V3 post-link dissent) are restated in owner-decisions-and-risks.md "Dissents", so little is lost. |
| 5 | Second copy of ARCHITECTURE-SPINE.md: keep issues/409/bmad/spec-orca-observer/ARCHITECTURE-SPINE.md, archive issues/409/bmad/architecture-orca-observer/ARCHITECTURE-SPINE.md (`cmp`: identical, 54,129 bytes each). Also archive architecture-orca-observer/reviews (4 files, 59 KB) and inputs (3 files, 37 KB) and .memlog.md (10 KB). | 54 KB duplicate, about 160 KB with reviews and inputs | SPEC.md and spec .memlog.md cite the spine by name; the code cites 24 distinct AD- and CD- ids from it (src/superclaude/cli/observe and tests/observe), so the spine itself earns its place once. final-review JSON cites both paths. | Low for the duplicate. If a reader has the architecture folder path bookmarked, they get a missing file; leave a one-line pointer. |
| 6 | UX folders: keep one of ux-orca-observer or ux-orca-observer-r2-review (both hold DESIGN.md and EXPERIENCE.md; the r2 copy is 44,581 bytes, the first 77,618 bytes). No live doc, code or test cites either path (grep found none). Which one is current is UNVERIFIED; the r2 folder follows git commit e64813a "UX design review of the release 2 panel", so probably r2. Archive the other plus both validation-report.html (61 KB and 94 KB), review-rubric.*, review-adversarial*.json, fix-log.md, .working (128 KB of extract JSON). | about 500 KB of 688 KB | No code, test or live doc. final-review verify files cite them. | Medium: the UX files are the only place for panel layouts; confirm which is current before archiving the other. |
| 7 | PRD process files: issues/409/bmad/prd-orca-observer extract-*.md (3 files, 75 KB), reconcile-*.md (3 files, 28 KB), polish-*.md and .json (12 KB), adversarial-review.json (10 KB), review-rubric.md (16 KB), validation-report.md and .html (26 KB), .memlog.md (6 KB). Keep prd.md and addendum.md. | about 175 KB of 260 KB | Nothing outside the folder (grep). | Low. Pure build scaffolding. |
| 8 | Unverified-register rows that change nothing now (my judgement, 8 of 25 rows): proof (a) "withdrawn" (history), Q-3 `ask` ("no R2 behaviour depends on it"), inbox lease fields (repeats row 1), "what identifies a human question" (decided 2026-11-11), production-integration reading (moot, see Gates), stack-table facts (nothing run, stack decided), AC-1..AC-10 restated, Orca reply sender (future stage, already in write-back-future-stage.md). Fold the useful remainder into one "forbidden verbs and withheld fields" list. | about 3 KB | unverified-register.md is cited by SPEC.md, prd.md and owner-decisions-and-risks.md; no code reads it. | Low. |
| 9 | handoff-step1 to 5.md (17 KB) and handoff-mvp-brainstorm.md. Each is a snapshot taken before the later decisions and carries the stale "not passed" lines. Referenced only by history files (prd extract and reconcile files, ux and architecture extract inputs, final-review/progress.md). | 17 KB plus handoff-mvp-brainstorm.md | Not by code or live docs | Low; archive with their folder. handoff-mvp-brainstorm.md is untracked; commit or copy before moving. |
| 10 | owner-decisions-20261112.md (executor-typed twin of the owner's pass record, 1.4 KB). release-gates.md line 38 already calls it "history, not the gate record". Fold its one useful fact (who typed it) into the pass record's neighbour, or archive. | 1.4 KB | release-gates.md:38 (in text); the code and its test read only owner-pass-record-20261112.md | Low, but release-gates.md must be edited in the same change or its text points at a missing file. |
| 11 | Binary packages: orca-observer-design-package.zip (14 MB, README says it is a copy of the canonical /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106, 52 MB) and attachments (4.3 MB, README says the issue already embeds them through GitHub assets). This is disk, not reading cost. | 18 MB | issues/409/README.md, package-manifest.json, attachment-status.json, posted-body.md, issue-body.md | Medium: README links the zip as "download the complete package". Owner decision; I list sizes only as instructed. |

Files that read as dead weight but are tiny (leave alone): flags.md, scout.md, draft-notes.md, description.md, create-result.json (the README names them as the issue-creation record).


## Gates: what each blocked or changed

Evidence is from reading release-gates.md, grep of src and tests, git log and the reflect and plan folders.

| Gate | What it blocked | What it changed | Verdict |
|---|---|---|---|
| DIRECTION-SELECTED | In practice nothing. Zero hits in src and tests. No owner-written selection record exists (handoff-mvp-brainstorm.md:35, release-gates.md:10). R1 was built and `superclaude observe` was registered (git 9e2608b03, PR #503; tests/observe/test_registration.py) on the owner's chat authorization (reflect assumption A-002, see Single source of truth row 1a). The gate text says the stricter reading ("offline R0 work only", release-gates.md "Production integration" section) still applies, which contradicts the shipped state and the QUESTION-OBSERVATION pass on line 38 of the same file. | Produced the "R0 only" paragraphs now stale in 7 live files; added open questions OQ-1 and OQ-2 and the AC-S reviewer check; the invariant behind it (INV-019) is "resolved in the design only" (handoff-mvp-brainstorm.md:71). Original purpose, keeping a human in charge of the visual direction, was met by the owner choosing the staged order on 2026-11-08 (owner-decisions-20261108.md item 1). | Process theatre in its present form. Smallest fix: the owner says in one sentence that the staged choice of 2026-11-08 plus the 2026-11-10 authorization satisfies it; record that in release-gates.md and delete the OQ-1, OQ-2 and AC-S text. This needs the owner's word; an agent must not write the selection record. |
| QUESTION-OBSERVATION | Real block. src/superclaude/cli/observe/commands.py:67 `QUESTION_GATE_PASSED` kept `--questions` from making any Orca call (T56, tests/observe/test_commands.py around lines 621 to 700), and the test at lines 741 to 750 refuses `True` unless a cited owner record file exists. | The gate research (27 evidence files, per release-gates.md line 38) changed the design: `--run` turned out to be a fence not a filter (consumer_fenced), so the planned rotation across Runs was removed and one named Run is the rule; the cap applies after `--types question` (41 rows against 100), so the argv always carries the type filter (T53); Q-1 FAIL produced the panel text and T52; non-consumption test T51. The owner passed it on 2026-11-12 on written terms. | Earns its place. |
| QUESTION-LINK | Nothing. Zero hits for the name or for Decision Desk in src and tests; R3 does not exist. | 90 mentions across 12 live files, plus OQ-13 to OQ-15 style open questions about a view that is not built. | Keep one line (a gate row and the "not established" list). Drop the repeated explanations in PRD, UX and handoffs. Low cost either way. |
| Cross-host joins (R4) and the "Later" rows | Nothing, no code. | A few table rows. | Fine as table rows. Do not give them a gate section. |
| Data-gate rule (four recorded samples: success, missing, stale, contradictory) | Real block. tests/observe/test_golden_contract.py pins 4 worker-list golden samples and 4 question samples; fixtures golden-*.json and golden-question-*.json ship in src/superclaude/cli/observe/fixtures. | A gate cannot be passed on a single happy-path sample. | Earns its place. |
| The honesty label on the questions panel | Enforced: src/superclaude/cli/observe/view.py:55, 4 test hits; the owner accepted it by name in owner-pass-record-20261112.md. | Keeps the screen from claiming "no questions". | Earns its place. |

### Acceptance tests T1 to T56 against tests that exist

- 402 test functions in 29 files under tests/observe (9,639 lines) cite 52 of the 56 ids by name in docstrings or names; 4 are never cited: T7, T17, T45, T50. T50 is a reviewer check on design images (acceptance-tests.md line 56: "R0 renders of A, B, C"), not a test. T7 (base fixture, 8 orchestrators), T17 (per-owner counts sum to global) and T45 (`read k of N Runs since start`) have no test citation; the string `read k of` and `Runs since start` appear nowhere in src or tests, so T45's header text is not built. Whether T7 and T17 are covered under another name is UNVERIFIED.
- The table does not match the code on three points: acceptance-tests.md says the snapshot schema test has "no ID assigned" (it exists: tests/observe/test_snapshot_schema.py); AC-S and the manual CJK check are reviewer-only and never run; there is no mechanism that checks the T-ids, so citation is by docstring habit only.
- Smallest fix: strike T45 and T50 from the list (or mark them "not built, reviewer check") and add the schema test id.

## Not checked

- The contents of orca-observer-design-package.zip (no `unzip` on this host) and the 52 MB canonical design folder.
- The 22 PNG attachments (sizes only, as instructed) and any HTML or PDF design export.
- Line-by-line drift of Q-1 and `consumer_fenced` across the 15 files that mention it (UX EXPERIENCE.md files hold 59 hits together).
- Whether the owner read owner-decision-pack.md (32 KB) or ran live-test-guide.md: no record found, UNVERIFIED.
- Whether the plan text cited as "plan:22" in the reflect diff-analysis really records the DIRECTION-SELECTED clearance; I read the reflect line, not the plan.
- Exact tracked status of every file in the brainstorm and tuibbs-review folders beyond the counts (0 tracked in the brainstorm).
- tuibbs-review internals (132 KB, 9 files): measured only. notes-1 to 3 and summary-check.md look like working notes; not read.
- The three finished design-doc rounds in .dev/reflect (about 400 KB across the pre-buildRelease1OfT-*, pre-planSourceV2-*, pre-release2OfTheOrc-* folders) and the two plan folders under .dev/tasks/done (about 2 MB): out of the stated scope, measured only.
- I did not run the tests; the citation counts are by grep, not by execution.

Risk to know: item 4 (brainstorm) and the untracked owner-decisions-20261108.md and handoff-mvp-brainstorm.md exist only on this disk; copy before anything is moved.
