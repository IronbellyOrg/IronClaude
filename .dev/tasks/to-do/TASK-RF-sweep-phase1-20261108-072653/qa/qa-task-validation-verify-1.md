# QA Report: Task integrity, fix verification (cycle 1)

**Task file:** TASK-RF-sweep-phase1-20261108-072653.md (2856 lines, 350 items)
**Date:** 2026-11-08
**Phase:** task-integrity, lens fix-verification
**Fix cycle:** 1
**fix_authorization:** false (report only; the task file was not edited)

Status: COMPLETE

## Overall Verdict: FAIL

25 of the 26 blocking findings are fixed. One (b2-p2 I1) is only partly fixed. One further blocking defect is in the file: the impl-cli gate is below the I22 full-intensity type floor. It predates the fixes, but the gate-floor check asked for here catches it. Open blocking count `|F_1|` = 2, against `|F_0|` = 26, so the count shrinks strictly and no monotonicity halt applies.

## Items Reviewed

| Finding ID | Fixed | Evidence |
|---|---|---|
| B2-01 | yes | `grep -cE 'Same inputs as\|as in item\|Apply the item\|HALT-item procedure\|decision-record form\|checks from item 2\.7'` = 0. Lens items restate full inputs, for example 2.8 (line 293): "spawn one `rf-qa` agent ... with this report-only preamble, verbatim" followed by the lens prompt and "Pass it the input list in Context". |
| B2-02 | yes | Fix and verifier items name full paths, for example 2.18 (line 363): "Pass it `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b1/consolidated-findings-cycle0.md`". `grep -noiE '(see\|as in\|same as\|like\|per) items? N.M'` returns nothing. |
| B2-03 | yes | 6.14 (line 1073) states the dedup rule "two findings are one finding when they name the same `file:line` and the same defect; keep the highest severity" and builds `F_0` and the cycle-0 PASS set. 6.18 (line 1101) and 6.22 (line 1129) state steps (a) regression, (b) monotonicity, (c), (d), each with the full HALT rule inline. 7.9 and 7.10 (lines 1198-1211) restate the record parts and Branch 1 and Branch 2. Phase 7 intro still says "follows the item 6.2 procedure", but every HALT item restates both branches (MINOR M2). |
| B2-04 | yes | `grep -c 'You are an adversarial reviewer'` = 111 (110 lens items + 1 shared copy); `'You are a verifier'` = 57 (56 + 1); `'You are the single fix agent'` = 29 (28 + 1). |
| B2-05 | yes | research/04 lines 87-95 hold edits 1 to 9 in order. Items cite 2.1 `:87-89` (edits 1-3), 2.2 `:90` (edit 4), 2.3 `:91-92` (edits 5-6), 2.4 `:93-94` (edits 7-8), 2.6 `:95` (edit 9); titles match. |
| B2-06 | yes | 2.2 Action (line 251) makes "the two replacements of research/04 section 2.2 edit 4"; Verification (line 253): "`grep -c 'or on a row with no observable start time, does not join' ...` returns 0; `grep -n 'A match on a row with no observable window does not join' ...` returns one hit ... contains `Dispatch time window not observable`". The text matches research/04:90. |
| B2-07 | yes | 7.16 Action (line 1259): "(1) Run template 2 (`orca-ide orchestration worker-list --run <run> --json`) once to learn the Dispatch ids ... (2) The "before" reads: template 3 for each Dispatch id from step 1". |
| B2-08 | yes | 7.16 Context: "The ccsession tab-map folder is `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/` (DESIGN line 32)". Action step (6) resolves and records it; Verification: "every file read for capture item 13 lies inside the recorded ... path". |
| B2-09 | yes | 7.20 (line 1286): "(expect at least 1 for each of the OQ-1 to OQ-7 files ... and 0 for the OQ-8 Run-id file)" and "`git status --short --untracked-files=all tests/sweep/fixtures/` (expect only lines starting `?? tests/sweep/fixtures/` that name a `captured-*.json` file or `SOURCES.md`...)". |
| b2-p2 I1 | partly (BLOCKING, see V-01) | `TASK_DIR` appears once, at line 169 ("no command relies on a `TASK_DIR` shell variable"). 14.43 (line 2726) uses `BASE=$(cat .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/base-commit.txt)` and `mkdir -p .dev/tasks/to-do/.../reflect/post`. 14.8 Branch A writes to `"$WT/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt"`. Branch B (line 2481) still says "saves output plus exit code to artifacts/sweep-help-pipx.txt". |
| b2-p2 I2 | yes | Same rebuild as B2-03. Every consolidation and decision item in Phases 8, 9, 10, 13 and 14 has the restated procedure; the phrase grep returns 0. |
| b2-p2 I3 | yes | Same preamble counts as B2-04. |
| b2-p2 I4 | yes | 8.11 Action (line 1488): "remove the `raising=False` argument from the `monkeypatch.setattr(probes, "_orca", fake, raising=False)` call"; Output lists `tests/sweep/conftest.py`; Verification: "`grep -n 'raising=False' tests/sweep/conftest.py` prints nothing". |
| b2-p2 I5 | yes | 9.1 Context lists the `[sweep publish]` messages; Verification greps `output dir escaped`, `report name space exhausted:`, `temp file exists:`, `cannot link report:`, `could not remove temp file`, plus a recorded check of the `makedirs` branch, which makes six. |
| b2-p2 I6 | yes | 9.3 Action (0): "confirm the `ALLOWED_ORCA` entry is `("orchestration", "worker-list", "--run", "<run>", "--json")`; if it differs, apply the HALT rule before any live call"; (1) "Run exactly `orca-ide orchestration worker-list --run <id> --json`". |
| b2-p2 I7 | yes | 11.1 Verification (line 1947): "`grep -nP '(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md'`". 11.4 Action (line 1966): "`re.search(r"(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md", activation)`". |
| b2-p2 I8 | yes | 10.1 Action (line 1771) names the closed set of eight files from `synthetic-run-current.txt` to `synthetic-worktree-current.json`; other variants are built "in memory or under `tmp_path`". |
| b2-p2 I9 | yes | 8.1 Action (line 1418): six `gate-decision.md` paths including `qa/r5/` ("expect 6 lines") and a loop over eight named OQ files ("expect 8 lines starting `OK`"). |
| sp1 I-1 | yes | Items 6.5 to 6.22 exist (lines 1008-1127): 5 rf-qa (4 + SPEC-fidelity domain lens 6.13) + 4 rf-qa-qualitative = 9, which is the 500-1500 row of 8 plus a domain lens (task-builder SKILL.md:1160). Phase 6 intro: "closed by its own QA gate (items 6.5 to 6.22, folder `.../qa/r5/`), before any Phase 7 item runs". |
| sp1 I-2 | yes | Items 7.21 to 7.28: 4 rf-qa (3 + read-only safety lens 7.24) + 3 rf-qa-qualitative + 1 rf-analyst = 8. Item 7.29 consolidates "the eight reports". |
| sp1 I-3 | yes | The report-only preamble requires a `## Checks` table (line 186 onward); 6.14 writes "the cycle-0 PASS set" and creates `cycle-ledger.md`; 6.18 appends the cycle-1 PASS set and runs regression against the cycle-0 set. `grep -c 'cycle-ledger.md'` = 226. |
| sp1 I-4 | yes | `grep -c 'in the SAME message, in parallel'` = 168. Key Constraints (line 156) states the rule. |
| sp1 I-5 | yes | 9.1 cites `src/superclaude/cli/sprint/recovery.py:424-434` and `src/superclaude/cli/swarm/atomic.py:28-31`. On disk, recovery.py:433 is `os.link(tmp_name, lock_path)` and atomic.py:31 is `os.fsync(handle.fileno())`. |
| sp2 I1 | yes | `### Follow-Up Items Identified` at line 2843 holds the #446 WC-9 entry and the other two entries; 14.42 says the section "still holds its three original entries plus one line per new follow-up". |
| sp2 I2 | yes | Gates 11.6 to 11.21 (`qa/cmd-skill/`) and 12.6 to 12.21 (`qa/contract/`) each have 3 rf-qa + 3 rf-qa-qualitative + 1 domain lens = 7, then one fix agent and two verifiers per cycle. |
| ORCH-R5 | yes | 11.1 creates `sweep.md` and 11.2 (line 1950) is "Step 1.20, routing row R5: add `"sweep"` to `_POST_REFRESH_ADDITIONS`": "This item therefore runs directly after item 11.1, and no item between them runs a test". Cross-references checked: 7.9 "Blocks: items 8.12 and 11.3" (11.3 is the SKILL.md step that needs OQ-6); 13.6 "step 1.16 (item 11.4)"; OQ-9 "(item 11.3)" (the skill holds the `:*` form); 11.4 "sweep.md (item 11.1) and SKILL.md (item 11.3)". |

## New-defect checks

| Check | Result | Evidence |
|---|---|---|
| Broken item cross-references | PASS | Every `item(s) N.M` reference (224 distinct ids) was extracted and compared with the 350 item ids using `comm`: none is missing. References inside the renumbered ranges (7.21-7.37, 11.x, 12.x) were read in context and point at the right items. |
| Gate below the I19/I22 floor | FAIL (V-02) | Lens tally by gate and type: r3-b1, r3-b2, r3-b3, r4 and r5 each 5+4; decisions 4+3+1 analyst; impl-core 4+3; **impl-cli 5 rf-qa + 2 rf-qa-qualitative**; tests 4+3; cmd-skill 4+3; contract 4+3; docs 5+3; final 6+4; fidelity 3+1. |
| Leftover `${TASK_DIR}` | PASS | `grep -c TASK_DIR` = 1, the convention sentence at line 169. |
| TBD, TODO, FIXME | PASS | All 23 hits (lines 285-1108) are quoted DESIGN checks such as `grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md` or lens prompts saying "no `TODO` or `TBD`". None is a placeholder. |
| Phase order | PASS | Phases 2-5 are design fixes with their gates, Phase 6 is R5 (HALT 6.2 at line 987) plus its gate, and Phase 7 holds the 1.0b HALTs (7.2-7.12) and the OQ-8 HALT 7.15. No Phase 1-7 Action creates or edits `src/` or `tests/`, except 7.18 (fixture copy, line 1270), which comes after every HALT. 8.1 pre-flight checks all six gates and eight records before any code. |
| New commit, push or merge item | PASS | `grep -noE 'git (commit\|push\|merge\|rebase)\|gh pr (create\|merge)'` hits only line 1279: `git merge-base --is-ancestor`, which is read-only. 14.45 runs `git add .dev/tasks` only. |
| POST reflect runner prompt | PASS | The 9 quoted lines of `~/.claude/skills/task-builder/SKILL.md:2223-2231` were substituted (`{TASK_FILE}`, `{OUTPUT_DIR}`, `[--spec {SPEC_PATH}]`, `{DEPTH}`, `{BASE}..HEAD`) and compared with task lines 2735-2743 using `diff`: IDENTICAL. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| V-01 | IMPORTANT | Item 14.8 Action, Branch (B), line 2481 | The halt line tells the coordinator to save the pipx output "to artifacts/sweep-help-pipx.txt". Commands run from the repository root, so this is the project-root `artifacts/` folder, which is never staged. On resume the item reads and verifies `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt` (Output, line 2482), so the check fails and the task halts again. This is the exact defect b2-p2 I1 named for 14.8; only Branch A was fixed. | In the Branch (B) `blocker_reason`, replace `artifacts/sweep-help-pipx.txt` with `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt`. |
| V-02 | IMPORTANT | impl-cli gate, items 9.5-9.11 (lines 1651-1693) | The gate has 5 rf-qa (9.5, 9.6, 9.8, 9.9 and the domain lens 9.7) and only 2 rf-qa-qualitative (9.10, 9.11). At `QA_INTENSITY: full` (BUILD-REQUEST:29), I22 requires "3 rf-qa + 3 rf-qa-qualitative per I19, plus domain lenses" (task-builder SKILL.md:1009, also :1172), and gates below it "are PROHIBITED and will be REJECTED during A.10.5" (:1010). The other code gates (impl-core, tests, cmd-skill, contract) all use 3+3+1. This predates the fixes: structure-p2 check 4 accepted the total of 7 against research/09 Gap 5 ("at least 6 for a code gate") and did not check the split. | Change one non-domain rf-qa lens (9.8 registration or 9.9 live-check evidence) to `rf-qa-qualitative` with a qualitative lens, or add an 8th rf-qa-qualitative agent. Then update "of 7" or "of 8" in the titles, the consolidation count in 9.12 and the parallel-spawn range. |
| M1 | MINOR | Halt lines in 6.2, 7.2, 7.4, 7.15, 14.7 and others; the 14.15 lens prompt (line 2530) | Halt lines name `phase-outputs/plans/OQ-*.md`, and the 14.15 lens prompt says "artifacts/base-commit.txt", both without the task folder prefix. Each item's Context gives the full path, and these are owner-facing pointers or reads with a full-path input, so behaviour is unaffected. | Optional: prefix the task folder. |
| M2 | MINOR | Phase 7 intro, line 1140 | "Every HALT item below follows the item 6.2 procedure" is a cross-reference, but each HALT item restates both branches, so it is redundant rather than load-bearing. | Optional: drop the clause. |
| M3 | MINOR | 14.44 runner prompt | `{BASE}..HEAD` is filled with a diff-file path, so the literal `..HEAD` disappears too. This is documented in OQ-12, required by BUILD-REQUEST:52, and accepted by reflect SKILL.md:80 (b2-p2 note). It counts as a placeholder fill. | None. |
| M4 | MINOR | Fidelity gate, items 14.29-14.32 | 3 rf-qa + 1 rf-qa-qualitative. I21/M4 fixes no 3+3 split for a fidelity gate, and research/09 Gap 5 sets the fidelity floor at 2, or 3 to 4 when sources exceed 1000 lines. Within that floor. | None. |

## Summary

- Blocking findings checked: 26. Fixed: 25. Partly fixed: 1 (b2-p2 I1, see V-01).
- New or remaining blocking defects: 2 (V-01, V-02), both IMPORTANT, 0 CRITICAL.
- Minor notes: 4 (M1-M4). They do not fail the gate.
- Monotonicity: `|F_0|` = 26, `|F_1|` = 2, a strict shrink. No item that passed at cycle 0 regressed. Cycle 2 of 2 remains available.

## Recommendations

- Fix V-01 and V-02 in one fix pass (cycle 2), then re-verify only those two plus the item renumbering in Phase 9 if V-02 adds an agent.

**Confidence:** Verified: 33/33 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 8 | Glob: 0 | Bash: 18

## QA Complete

VERDICT: FAIL
