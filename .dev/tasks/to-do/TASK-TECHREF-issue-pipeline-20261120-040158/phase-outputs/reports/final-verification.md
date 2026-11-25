# Final verification (Step 7.1)

## 1 wc -l
$ wc -l DOC
2436 /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
Tier: Standard target about 800-1,300 lines plus appendices; actual 2436 lines, ABOVE the target band (information only; accepted tier decision recorded in research-notes.md and tier-decision.md). PASS (informational)

## 2 headers
$ grep -n "^## " DOC
78:## Document Information
102:## Completeness Status
138:## Table of Contents
183:## 1. Overview
224:## 2. Architecture
364:## 3. Directory Structure
444:## 4. Data Flow
655:## 5. Subsystem Reference
1368:## 6. State Management
1397:## 7. Component Inventory
1403:## 8. API & Integration Points
1512:## 9. Configuration & Environment
1579:## 10. Error Handling & Edge Cases
1651:## 11. Performance Characteristics
1698:## 12. Conventions & Patterns
1747:## 13. Extension Guide
1876:## 14. Known Limitations & Technical Debt
2025:## 15. Verification & Accuracy
2148:## 16. Glossary
2203:## Appendix A: Test-Pin Matrix
2279:## Appendix B: Removed on 2026-11-20
2426:## Document History
numbered headers 1-16 found: 16; Appendix A: 1; Appendix B: 1
PASS

## 3 placeholders
$ grep -n -E '\[placeholder|TODO|TBD|PLACEHOLDER|YYYY' DOC
(exit 1; 1 means no match)
PASS

## 4 PR 686 / rewrite design
1
218:PR 686 and the rewrite design are out of scope for this reference.

## 5 memory-note terms
20
231: TRIGGERS   (a scheduler, dispatcher or zero-setup install is "not found in snapshot")
330:| 7 Coordinator text, issue-pipeline duties | NOT BUILT | `src/superclaude/core/WORKER-CONTRACT.md` (full read: no "Issue pipeline duties", no "WC-17", no "watcher", no "COORD-"); issue-related lines only at `:23, 57, 66, 242-
340:| 15 Dispatcher, `COORD-<RepoName>` coordinator worktree, zero-setup install | NOT BUILT | not found in snapshot: `COORD-` has 0 hits outside `.git` and `.dev`; `dispatcher` hits are unrelated (swarm, Orca shim) | none | none 
566:| Scheduler, dispatcher, `COORD-` coordinator worktree, zero-setup install for the issue pipeline | not found in snapshot (no cron, timer, workflow, Orca automation or such artefact; `COORD-` has zero hits) | not found in snap
671:| Dispatcher, `COORD-<RepoName>` worktree, zero-setup install | not found in snapshot (`COORD-` returns 0 hits; no dispatcher for the issue pipeline) | not found in snapshot |
915:Prose-only gates (no code check): the live-test record, shadow run, grants, acceptances and a running coordinator (SET:226-290, 584-635); "grant row" appears only as prose (SET:274, `docs/designs/issue-pipeline-fu1.md:24, 26`)
948:| Dispatcher, `COORD-`, zero-setup install, coordinator that starts the worker after the claim | not found in snapshot | research 03 F.2, F.3; the "Issue pipeline duties" contract text is REMOVED (CHANGELOG.md:17) |
1348:**Explicit finding.** `WC` has no WC-17 and no heading or sentence "Issue pipeline duties" (0 grep hits each), and no "issue pipeline", "watcher", "adopt", "claim" or "COORD-" text; "dispatcher" and "zero-setup watcher" are l
1350:**Issue-related lines in the contract** (grep of `issue`, `grant row`)
1355:| 57 | WC-3 sub-bullet: "other owner records, such as a grant row or a pass record, are still written by the owner" | the phrase "grant row" occurs exactly once; the contract defines no store, writer verb or schema for it (a 
1904:| KW-3 | `SET:170`; `SET:616-619`; `SET:5`, `SET:270-274` | Cites `WCT` section 4 "Issue pipeline duties"; launch capture command is `--prompt '/sc:issue --claim <test issue>'`; a live-test file is a deliverable; no dispatche
1931:| X-17 | `SET` section 8.5 | Relies on a "grant" and a coordinator handoff | No dispatcher, no zero-setup step; no code implements a grant or handoff | [STALE DOC] | R03 |
1967:| D-16 | Coordinator hand-off after a claim (adopt, create the issue worktree, `worker-start`); dispatcher, `COORD-<RepoName>` worktree, zero-setup install | `DES:43`; `SET:170`; `docs/designs/issue-pipeline-fu1.md:9-12`; `sr
2000:| U-3 | Whether `enabled` is true in the owner's real config; whether any Coder cron, dispatcher, coordinator, external scheduler or person runs `issue-watch once` | No config or scheduler artefact in the snapshot; "dispatche
2048:| 8 | No dispatcher or `COORD-` worktree exists for the issue pipeline (Sections 2.3, 4.4) | no output |
2078:grep -rIn 'COORD-' "$S" --exclude-dir=.git --exclude-dir=.dev
2107:A snapshot has no runtime state, no git history and no PR data. The tests were read, not run. Only the L1 guard script was executed, once, against 44 sample payloads in a sandbox HOME (Section 5.3 observation run); the identi
2337:- The contract text told the coordinator model to write to GitHub without a command line: "Post the plan reply with the hash and file list and mention the assignee" and "mirror the label and Status" (old `WCT:298`); "post an 
2354:| 6 | Never (`:300`) | Tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker alone; "post an issue write without that issue's grant row" |
2356:Facts about names: the duties named `adopt-create`, `adopt-mark`, `stage-status`, `record-create`, `record-mark` (and WC-17 named `plan-hash`, `check-approval`), never `release-worker` or `brief`. "COORD-" was absent from the

## 6 snapshot fingerprint
baseline (phase1-scope-confirmation.md): f20de643086d06b8c8cffb981676a619719094036d6fa386953b4bc777d49b74, 2178 files
f20de643086d06b8c8cffb981676a619719094036d6fa386953b4bc777d49b74  -
2178

## Results per check
1. wc -l: 2436 lines, above the Standard band (informational): PASS (informational).
2. Headers `## 1.` to `## 16.` in order plus Appendix A and Appendix B: PASS.
3. Placeholders: 0 hits: PASS.
4. PR 686 / rewrite design: exactly 1 hit, line 218, in Section 1 (starts at line 183): PASS.
5. Memory-note terms: 20 hit lines; the hits read as "not found in snapshot" rows or as quoted facts about file contents (WORKER-CONTRACT.md:57 contains "grant row" once; the removed contract text and old docs use it), none states them as an existing system: PASS.
6. Snapshot fingerprint after = baseline (f20de643..., 2178 files), identical: PASS. (Root directory mtime changed earlier through a removed probe file created by an earlier QA agent; regular files unchanged.)
