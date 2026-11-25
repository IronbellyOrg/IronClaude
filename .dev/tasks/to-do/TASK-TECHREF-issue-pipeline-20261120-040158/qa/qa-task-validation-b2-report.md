# QA Report - Task Integrity, Lens b2-self-containment

**Task file:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/TASK-TECHREF-issue-pipeline-20261120-040158.md
**Date:** 2026-11-20
**Phase:** task-integrity (lens b2-self-containment)
**Fix authorization:** false (report only)

## Progress log (appended incrementally)

- Started. Read all 2,365 lines of the task file in chunks, BUILD-REQUEST.md in full, research-notes.md lines 40-131, and MDTM template 02 sections B1-B7 and I17.
- Mechanical sweeps over all 83 `- [ ]` items (Bash grep): every item contains `ensuring`, `cannot be marked as done` and `Once done, mark this item as complete`; every item has a blocker-logging clause (items 7.3 and 7.4 phrase it as "If the summary or verdict files are missing..." / "If the document or the verification file is missing..."). No `see above`, `as above`, `continue from` in any item. Item count is 83 (matches the stated 83).
- Snapshot spot checks of scout hints that the items embed: MAX_LAUNCHES_PER_CYCLE (cycle.py:35, only hit in src), SKEW_WARN_S=60 (cycle.py:44) vs doc 300 (docs/designs/issue-watcher.md:827), IR7_REFUSE=False (orca_worktree.py:822), IMPL case `implement | task | cleanup` (launch-level-guard.sh ~409), no WC-17 / "Issue pipeline duties" in WORKER-CONTRACT.md, no caller of `orca_worktree.py pending` (only argparse registration at :1893), T3 pin claude-gw-tier2b vs design claude-gw-tier3, docs/designs/issue-watcher-live-test.md absent, commit 01e7a9e23 readable via git. All hold, so the embedded hints are accurate at 61ac2c2e6.

## Lens checklist results

| # | Lens check | Result | Evidence |
|---|-----------|--------|----------|
| 1 | All 5 B2 components per item (context+why, action, output, verification, completion gate) | PASS | All 83 items have an output path or decision file, an `ensuring...` clause, a blocker-logging clause and the completion gate (grep sweep). Context-with-WHY is present ("because ..." in every spawn item; reads-with-purpose in file items). |
| 2 | No item relies on prior-item context without restating | PASS with Medium/Note findings | Gate 1/2/3/4 cycle-2 and Gate 4 items depend on another item's prompt block (M1, M2); group-level paragraphs hold the `[N]` rule, the synth-file Glob precondition and the Gate 4 precondition (N2, N3); c2 consolidation items point at another item for severity definitions (N4). |
| 3 | Agent-spawning items embed full prompts with SOURCE ROOT AND SAFETY block, Incremental File Writing Protocol, (research) Staleness Protocol + C8, (QA) adversarial stance | PASS for 39 of the 53 fixed spawn items (counted: 2.1-2.6, 3.1-3.3, 3.6, 3.7, 5.1-5.12, 5.14-5.16, 6.1-6.8, 6.10-6.12, 6.19, 6.20); the other 14 (3.11, 3.12, 5.19-5.21, 6.15-6.17, 6.22-6.24, 6.27-6.29) reuse a cycle-1 block by reference, and the 3.9 generator points at the Step 3.4 template (M1, M2) | Checked each fenced block: 2.1-2.6 carry safety block, incremental protocol, full 4-point Staleness Protocol, C8; 3.1-3.3, 3.6, 3.7, 5.7-5.12, 5.14-5.16, 6.2-6.8, 6.10-6.12, 6.19, 6.20 carry safety block, adversarial stance and incremental protocol; 5.1-5.6 carry safety block, rules 0-12 (rules 10/11 = staleness, F = C8), incremental protocol; 6.1 carries safety block (assembler variant) and incremental protocol. |
| 4 | Absolute, specific file paths | PASS with Note | No relative or `.../` path appears inside any prompt block. 19 item bodies use the `.../` shorthand after a full absolute path (N1). |
| 5 | Measurable verification | PASS | Counts, file existence, verdict words, F_n arithmetic, exact halt lines, grep commands in 7.1. Weak spots are generic ("nothing fabricated") but each item also has a countable check. |
| 6 | No batch items | PASS with Note | One agent per item throughout. 7.1 bundles six read-only checks into one result file and 7.2 checks many files; both write one output and are verification aggregates, not "spawn all X" batches (N5). |
| 7 | No item built on [CODE-CONTRADICTED]/[UNVERIFIED] findings | PASS with Medium finding | Phase 2 prompts hedge correctly ("re-verify each", "expected", "[CODE-CONTRADICTED candidate]"). Phase 5 item text and prompts then make several of the warnings mandatory output content (M3). I confirmed by reading the snapshot that the facts are currently true, so no wrong deliverable results. |

## Verdict on the known departure (cycle-2 and Gate 4 prompt reuse)

The builder's note (Builder Notes, "Cycle-2 prompt reuse") lists Steps 3.11-3.12, 5.19-5.21, 6.15-6.17, 6.27-6.29 and 6.22-6.24. My reading of the item bodies shows the same pattern also in Step 3.9 (gap-fill items for cycle 2 are "copied from the GAP-FILL ITEM TEMPLATE in Step 3.4").

Judgement: it is a real B2/B1 form defect (an item that tells the executor to "use the prompt of Step 6.10 ... copied in full ... with these substitutions" is not a complete prompt that can run without other context, which is exactly what B1 protects against after session rollover). It is NOT blocking, because (a) the referenced block is in the same file, by step number, and every referenced block is explicitly labelled as the authoritative template ("Complete prompt for Step 3.6 ... is also the template that Step 3.11 reuses"); (b) every reuse item names the output path, consolidated-findings path and fix-report path to substitute and states that the SOURCE ROOT AND SAFETY RULES, ADVERSARIAL STANCE, Incremental File Writing Protocol, grading and report format must be in the Agent call; (c) the items that need the safety block cannot lose it silently because the item text requires it. The practical risk is executor drift while pasting about 40 lines per call and an incomplete substitution list for Gate 1 (M2).

## Issues Found

### Blocking

None. No item, if followed as written, writes outside the task folder or the single output file, modifies the snapshot, stages or commits, calls GitHub with a write verb, uses web tools, or omits one of the four gates (Gate 1 at 3.1-3.14, Gate 2 at 5.7-5.22, Gate 3 at 6.2-6.18, Gate 4 at 6.19-6.30, plus 6.31 and 7.1). Every spawn prompt that touches files carries the six-bullet SOURCE ROOT AND SAFETY RULES block verbatim (only the parenthetical task-folder line differs: the assembler prompt in 6.1 says it is the only agent that creates the output file, and the 6.10 fix-agent prompt says it may edit it).

### Medium

**M1. Cycle-2 and Gate 4 spawn items reuse another item's prompt by reference (B2/B1 form defect, non-blocking).**
Items: 3.11, 3.12 (reuse the 3.6 / 3.7 blocks), 5.19, 5.20, 5.21 (5.14 / 5.15 / 5.16), 6.15, 6.16, 6.17 (6.10 / 6.11 / 6.12), 6.22, 6.23, 6.24 (Gate 4 reuses 6.10 / 6.11 / 6.12), 6.27, 6.28, 6.29 (6.10 / 6.11 / 6.12 again). Related: 3.9 tells the executor to generate gap-fill items "copying the GAP-FILL ITEM TEMPLATE from Step 3.4 with `c1` replaced by `c2` everywhere".
Quotes: 5.19 "using the prompt of Step 5.14 (the fenced block of Step 5.14, copied in full into the Agent call) with these substitutions"; 6.22 "using the prompt of Step 6.10 (the fenced block of Step 6.10, copied in full into the Agent call)"; 3.11 "the agent prompt MUST contain, verbatim, the same safety block, ADVERSARIAL STANCE line, Incremental File Writing Protocol, severity grading and report format ... that Step 3.6 requires".
Judgement: not acceptable as a pure B2 pattern (the item is not a complete prompt; the executor in a later batch must locate and re-read a block 80 to 230 lines earlier and apply substitutions by hand), but acceptable in practice because the block is on disk in the same file, is labelled authoritative, and the safety/stance/protocol requirements are named in each item. The Gate 4 reuse is slightly worse than the cycle-2 reuse: 6.23 and 6.24 take the Gate 3 prompts, whose PROCESS text checks "all 16 template sections present in order, Appendix A and Appendix B present, Table of Contents matches headers" (a Gate 3 check), and the substitution list only changes the QA-phase label, paths and one added process rule.
Required fix (optional, form only): inline the full block in each of the 14 items, or at minimum add the explicit list of strings to change ("cycle 1" to "cycle 2", `-c1` file names to `-c2`, the research-directory sentence in 3.11/3.12) as 5.20 and 6.16 already do.

**M2. Gate 1 cycle-2 items 3.11 and 3.12 give no substitution list.**
Unlike 5.19-5.21, 6.16-6.17 and 6.22-6.29 (which list "cycle 2, consolidated findings ..., fix report ..., output path ..." and, for 5.20/6.16/6.28, "previous review meaning ..."), 3.11 and 3.12 only name the consolidated-c2 and output paths. The 3.6/3.7 blocks contain hard-coded "cycle 1", "gap-fill-c1-*.md", "Gap-fill c1" and "review 1 had explicitly rated PASS" strings. For cycle 2 the "previously rated PASS" set (review 1 plus cycle-1 verification) is not defined in 3.11/3.12, although 3.13 step (1) runs the regression check from those reports. Result if followed literally: a cycle-2 agent is told to read only `gap-fill-c1-*` and to compare against "review 1", so a regression introduced by cycle-1 gap-filling could be mis-attributed. The deliverable (report with verdict and counts) still exists, so this is not blocking.
Required fix: add the substitution list and the definition of "previous review" for cycle 2 to 3.11 and 3.12.

**M3. Phase 5 items and prompts make scout hints and BUILD-REQUEST staleness warnings mandatory output content, although BUILD-REQUEST says "Do NOT create task items that build on any of these as if true".**
Examples: item 5.3 "ensuring the output ... contains ... the dead constant `MAX_LAUNCHES_PER_CYCLE` recorded with the real enforcement point, the skew 300 versus 60 contradiction tagged `[CODE-CONTRADICTED]`"; item 5.4 "the statement that the ccsession shim carries no launch level, and in 5.4 exactly what the snapshot contract says about issue-pipeline duties (no WC-17, no "Issue pipeline duties" section)"; synth-04 prompt "BUILT-OFF for IR-7 refusal (IR7_REFUSE = False); NOT BUILT for IR-3 pipeline.json and for any caller of orca_worktree.py pending"; synth-05 prompt "mark MAX_LAUNCHES_PER_CYCLE as defined but never read"; item 5.6 "the contradiction table has a row for every `[CODE-CONTRADICTED]` item ... (including the eight known staleness warnings from BUILD-REQUEST.md)"; synth-01 prompt ledger row "dispatcher / scheduler / zero-setup install (not found in snapshot)". The Phase 2 prompts hedge correctly ("re-verify each", "expected"), and 5.6 (14.1) and 5.8 check (l) say "as far as the research confirms or refutes each" / "present or explicitly refuted", but the Gate 2 severity text makes "missing required content item" BLOCKING, so a refutation by research would still be flagged.
Impact: none today, because I re-read the snapshot and every hint I checked is true (see progress log), so no wrong deliverable follows; it is a process-form violation of the BUILD-REQUEST directive and a latent contradiction if research disagrees.
Required fix: prefix each such clause with "if research file NN confirms it (otherwise record the refutation with evidence)", and make 5.3, 5.4, 5.5 match the wording already used in 5.6/5.8.

### Notes (form or wording only)

- N1 (path style). 19 item bodies use `.../` after a full absolute path: 1.2, 2.1, 2.2, 2.3, 2.4, 2.5, 3.9, 3.13, 5.13, 5.17, 5.18, 5.22, 6.13, 6.14, 6.18, 6.25, 6.26, 6.30, 7.2. No `.../` appears in any prompt block, so spawned agents always receive absolute paths. Spelling out the paths would meet "absolute, specific paths" literally.
- N2 (`[N]` placeholder). Prompts 6.2-6.8 contain "[N] errors" and the instruction to substitute N (recorded by 6.1, N = max(5, lines/100)) sits only in the Gate 3 header paragraph before 6.2. The items themselves do not say where N comes from; an executor that reads only the item would send a literal "[N]".
- N3 (preconditions in group paragraphs). "Glob synthesis/synth-0*.md and confirm six exist" (before 5.7-5.12) and "Gate 4 runs only after gate3-verdict.md contains PASS" (before 6.19-6.20) are in the group paragraphs, not the items. Harmless because every HALT step says STOP executing all further items.
- N4 (severity definitions by reference). 3.9, 5.18, 6.14 and 6.26 say "same BLOCKING/MINOR definitions as Step 3.4 / 5.13 / 6.9 / 6.21" instead of restating them. The c2 consolidation only copies BLOCKING findings already graded in the verification reports, so the practical risk is low.
- N5 (aggregate items). 7.1 runs six checks and writes one result file; 7.2 checks many files and writes one table. They are verification aggregates, not "spawn all X" batch items.
- N6 (counts in item text). Step 2.1 says "a test-pin row for each of the six test files named in the prompt" and the agent header says "six test files", but the prompt names five (test_cycle.py, test_predicates.py, test_audit.py, test_marker_contract.py, conftest.py; research-notes row 01 also lists five). Step 2.4 says "list the 17 files"/"the 17 templates" but the snapshot templates directory holds 15 files (find -type f = 15; research-notes line 39 carries the stale 17). A literal executor may re-spawn agent 01 once for a sixth row that does not exist.
- N7 (safety wording). The block says "Do not read source from /home/coder/workspaces/IronClaude (that checkout is stale)", while synth, QA and assembler prompts direct agents to read the template and task-folder files under `/home/coder/workspaces/IronClaude/.claude/templates/...` and `/home/coder/workspaces/IronClaude/.dev/tasks/...`. The intent (code is read only from the snapshot) is clear, but one clarifying clause ("task folder, templates and BUILD-REQUEST are not source") would remove a possible refusal or a QA false positive. Also, the 3.4 gap-fill prompt carries condensed Staleness and C8 text rather than the full four-point protocol of Phase 2; acceptable for a gap-fill agent.

### Out-of-lens observation (for the structure lens, not graded here)

I17.5 and I17.6 of template 02 call post-completion lens QA and a fidelity gate "MANDATORY ... before the task is marked Done", encoded as explicit `- [ ]` items. Step 7.3 instead records that they are "not repeated as separate runs" because Gates 3 and 4 in Phase 6 run on the same final document, citing BUILD-REQUEST's phase mapping. That is a documented deviation, but "Deviations from Process" in the Task Log is still empty and the Builder Notes carry the rationale. Document edits made by the Gate 4 fix agent are only re-checked by the Gate 4 verification round and the mechanical checks in 7.1, not by the Gate 3 lenses.

## Summary

- Checks passed: 7 of 7 lens checks, with 3 Medium findings and 7 Notes recorded.
- Blocking issues: 0. Medium: 3 (M1, M2, M3). Notes: 7 (N1-N7).
- Known-departure ruling: B2 form defect on 14 items (3.11, 3.12, 5.19-5.21, 6.15-6.17, 6.22-6.24, 6.27-6.29) plus the 3.9 template pointer; non-blocking; 3.11 and 3.12 are the weakest (M2).

## Confidence and tool engagement

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 23 | Grep: 6 | Glob: 0 | Bash: 7 (Read+Grep+Glob = 29 against 7 lens checks; Bash used for item-wide mechanical sweeps and snapshot spot checks)
- Self-audit: the 0-blocking result rests on the item-wide grep sweeps, a full read of all 2,365 lines, comparison of each spawn block against the safety/protocol/stance requirements, and snapshot re-reads of the scout hints; Mediums and Notes are listed because the cycle-2 reuse, the missing substitution list and the hard-wired hints are real departures from B2 and the BUILD-REQUEST directive.

VERDICT: PASS
