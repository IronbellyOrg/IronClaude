# A.10 task file validation, fix log (cycle 1)

Date: 2026-11-08
Task file: TASK-RF-sweep-phase1-20261108-072653.md
Fix agent: rf-qa, `fix_authorization: true`, cycle 1 of at most 2.
Inputs: qa-task-validation-consolidated.md and the four reports it names (b2-report-p1, b2-report-p2, structure-report-p1, structure-report-p2).

Status: COMPLETE. 26 blocking findings fixed (25 from the reports plus the orchestrator addition), 0 not fixed.

## Result in numbers

| Measure | Before | After |
|---|---|---|
| Lines | 2479 | 2856 |
| Checklist items | 297 | 350 |
| Items with all five fields (Context, Action, Output, Verification, Completion gate) | 297 | 350 |
| QA gates | 11 | 14 (new: `qa/r5/`, `qa/cmd-skill/`, `qa/contract/`) |
| Bytes | about 366 KB | about 919 KB (gate preambles and input lists are now restated in every gate item) |

Items per phase after the fix: 1: 4, 2: 25, 3: 23, 4: 24, 5: 30, 6: 22, 7: 37, 8: 29, 9: 20, 10: 24, 11: 21, 12: 21, 13: 25, 14: 45. Numbering is contiguous in every phase, and no `item N.M` reference points at a missing item (checked with grep and comm).

## How the fixes were made

- The repeated gate items (about 180 items in 14 gates) were rebuilt by a one-off generator script kept outside the task folder. It parsed each item by id, kept every lens prompt verbatim, restated inputs, preambles and rules, and asserted every anchor (exact match counts, five fields per item, the POST reflect runner prompt lines unchanged). The same script replaced `${TASK_DIR}` with the literal path, restated the decision-record form and the HALT branches in Phase 7, and moved routing row R5.
- Every other fix was a targeted Edit, each preceded by a Read of at most 150 lines.
- Phase order, the design-fix gates before any code, the R5 and 1.0b HALT behaviour, item meaning and scope are unchanged. No commit, push or merge item was added. The POST reflect runner prompt (item 14.44) is byte-identical (9 quoted lines compared).

## Findings

| ID | Report | Item(s) changed | Result | Notes |
|---|---|---|---|---|
| B2-01 | b2-report-p1 | Every lens item in all 14 gates (110 items) | FIXED | "Same inputs and gate folder as N" replaced by the full input list with paths, the gate folder and the explicit sizing. Lens-specific extras are kept as "Extra inputs for this lens" or "Focus for this lens". |
| B2-02 | b2-report-p1 | Every fix and verifier item (28 fix, 56 verifier) | FIXED | Inputs are full paths under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/<gate>/`, plus the gate input list. No "Same inputs as" remains (grep count 0). |
| B2-03 | b2-report-p1 | All consolidation, cycle-1 decision and gate decision items; mechanical items 3.5, 4.6, 5.12; decision records 7.1, 7.3, 7.5, 7.7, 7.9, 7.11; HALT items 7.2, 7.4, 7.6, 7.8, 7.10, 7.12 and their Context lines | FIXED | Each item now states the dedup rule, how `F_0`, `F_1`, `F_2` and the PASS sets are built, the HALT rule steps, the four common DESIGN check commands, the decision-record parts, and Branch 1 and Branch 2. Grep counts for "as in item", "Apply the item", "HALT-item procedure", "decision-record form" and "checks from item 2.7" are all 0. |
| B2-04 | b2-report-p1 | Every spawn item (110 lens, 56 verifier, 28 fix) | FIXED | The report-only, verifier and fix preambles are embedded verbatim in each spawn item. The Execution Context copies remain as the reference. |
| B2-05 | b2-report-p1 | 2.1, 2.2, 2.3, 2.4, 2.6 | FIXED | research/04 pointers corrected to :87-89, :90, :91-92, :93-94 and :95 (checked against research/04 lines 87 to 95). |
| B2-06 | b2-report-p1 | 2.2 | FIXED | Action now makes both edit 4 replacements; Verification checks that the old "or on a row with no observable start time, does not join" text is gone and the `Dispatch time window not observable` sentence is present. |
| B2-07 | b2-report-p1 | 7.16 | FIXED | Explicit order: (1) one `worker-list` call to learn Dispatch ids, recorded as an extra read; (2) before reads; (3) other templates and the fake-id call; (4) after reads; (5) version file; (6) tab-map folder. |
| B2-08 | b2-report-p1 | 7.16 | FIXED | Literal folder `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/` (DESIGN line 32), resolved and recorded before reading; Verification checks every read lies inside it. |
| B2-09 | b2-report-p1 | 7.20 | FIXED | Expected values added: at least 1 "does NOT authorize adoption" in each OQ-1 to OQ-7 file and 0 in OQ-8; `git status --short --untracked-files=all tests/sweep/fixtures/` must list only `??` lines for `captured-*.json` and `SOURCES.md`. |
| I1 | b2-report-p2 | Whole file (427 occurrences), Handoff File Convention | FIXED | `${TASK_DIR}` replaced by the literal `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` everywhere; the convention now says every command runs from the repository root and no command relies on a `TASK_DIR` variable. Items 14.4, 14.5, 14.8, 14.9 and 14.43 now write to the task package, not the project-root `artifacts/`. |
| I2 | b2-report-p2 | Consolidation and decision items in Phases 8, 9, 10, 13, 14 | FIXED | Same rebuild as B2-03. |
| I3 | b2-report-p2 | Every spawn item in Phases 8, 9, 10, 13, 14 | FIXED | Same rebuild as B2-04. |
| I4 | b2-report-p2 | 8.11 | FIXED | Action names the exact call to change; Output lists `tests/sweep/conftest.py`; Verification greps that `raising=False` is gone. |
| I5 | b2-report-p2 | 9.1 | FIXED | Context lists all six `[sweep publish]` messages from DESIGN lines 106-128; Verification greps each fixed part and records the `makedirs` branch line. |
| I6 | b2-report-p2 | 9.3 | FIXED | Literal command `orca-ide orchestration worker-list --run <id> --json` (or the same argv after `$ORCA_CLI_COMMAND` when set); a pre-check confirms the `ALLOWED_ORCA` entry `("orchestration", "worker-list", "--run", "<run>", "--json")` (DESIGN 7.3 line 523) before any live call; Verification compares the run argv with it. |
| I7 | b2-report-p2 | 11.1 Verification, 11.4 Action (was 11.3) | FIXED | The project copy is matched with a `(?<!~/)` lookbehind (`grep -nP` and `re.search`), so the installed path alone cannot pass. |
| I8 | b2-report-p2 | 10.1 | FIXED | Closed set of eight named `synthetic-*` files, one per `ALLOWED_ORCA` template that item 7.18 did not capture; all other variants are built in memory or under `tmp_path`. Output and Verification name the files. |
| I9 | b2-report-p2 | 8.1 | FIXED | Context names the eight decision files; Action checks each exists and holds `status: RESOLVED` (8 `OK` lines expected) and checks six gate PASS lines, including the new R5 gate. |
| I-1 | structure-report-p1 | New items 6.5 to 6.22; 1.2; Key Constraints; Phase 6 heading and intro; 6.4 Context; 8.1 | FIXED | R5 gate added after the decision is applied: 4 rf-qa + 4 rf-qa-qualitative + 1 domain lens (the 500-1500 line row), one fix agent, two verifiers, at most 2 cycles, folder `qa/r5/`. Item 1.2 creates the folder; the folder count is now 14. |
| I-2 | structure-report-p1 | 7.21 to 7.37 (was 7.21 to 7.34) | FIXED | Decisions gate raised to 8 agents: 3 rf-qa (completeness, new record-form, new evidence-quality) + 3 rf-qa-qualitative (decision-fidelity, downstream-actionability, new crossref-chain) + the rf-qa read-only safety domain lens + the rf-analyst cross-source lens. Titles say "of 8"; consolidation expects 8 reports; later items renumbered 7.29 to 7.37, and no reference outside the gate pointed at them. |
| I-3 | structure-report-p1 | Report-only and verifier preambles (Execution Context and every gate item); every consolidation and decision item | FIXED | Lens agents number their checks and end with a `## Checks` table; consolidation writes the cycle-0 PASS set and creates `cycle-ledger.md`; each decision item appends its cycle's PASS set, F set and count. Lens Verification lines check the table exists. |
| I-4 | structure-report-p1 | Every lens batch and verifier pair in all gates; Spawn rule; Key Constraints | FIXED | Each lens item says "spawn all of them in the SAME message, in parallel"; each verifier pair likewise (168 markers). |
| I-5 | structure-report-p1 | 9.1 Context | FIXED | Cites `src/superclaude/cli/sprint/recovery.py:424-434` (link at :433) and `src/superclaude/cli/swarm/atomic.py:28-31` (fsync), both checked on disk. |
| I1 | structure-report-p2 | Task Log; 14.42 | FIXED | Added `### Follow-Up Items Identified` with the WC-9 lock retry (#446), the OQ-1 branch (b) contract PR for line 110, and opening the PR via `/sc:pr-submit --monitor 3`; item 14.42 copies new follow-ups there. |
| I2 | structure-report-p2 | New items 11.6 to 11.21 and 12.6 to 12.21; Phase 11 and 12 headings and intros; 1.2; Key Constraints | FIXED | Cmd-skill gate (`qa/cmd-skill/`) and contract gate (`qa/contract/`), each 7 agents (3 rf-qa + 3 rf-qa-qualitative + 1 domain lens, the code-gate floor), one fix agent, two verifiers, at most 2 cycles. The docs gate stays as the cross-phase check. |
| ORCH-R5 | consolidated (orchestrator addition; minor M1 in structure-report-p2) | 11.2 (was 11.4), 11.3 (was 11.2), 11.4 (was 11.3); 7.9; 13.6; OQ-9; Phase 11 intro | FIXED | Routing row R5 now lands directly after `sweep.md` is created, before any test run (research/03 ordering constraint 2, line 109). Cross-references updated: 7.9 blocks 11.3, 13.6 cites 11.4, OQ-9 cites 11.3, 11.4 names its files. |

## Extra fix, not in the reports

| Item | Change | Reason |
|---|---|---|
| 6.3 Verification | `grep -n 'never include \`--agent-wait\`'` replaced by `grep -n 'probes never include'` plus a check that the line holds `--agent-wait` | In GNU grep a backslash before a backtick is a start-of-buffer anchor, so the old command could never match. The R5 gate depends on this check. |

## Minor findings

Not fixed unless a blocking fix covered them. Covered by blocking fixes: M-06 (b2-p1, sizing now explicit in every lens item), M1 (b2-p2, sibling "Same inputs" removed), M1 (structure-p2, the R5 move). All other MINOR notes, including M6 and M10 in structure-p1 and structure-p2 (the `Verify on branch (b):` prefix in item 6.3), remain recorded in the four reports and are unchanged.

## Risks for the re-review

- The task file is about 2.5 times larger. Gate lines are long, so a 150-line chunk can exceed a reader's per-call token limit; readers may need smaller chunks.
- The new lens prompts for the R5, cmd-skill, contract and decisions gates are builder-written in the style of the existing lenses and from DESIGN sections 7.6, 8 and 9; no second reviewer has checked them yet.
