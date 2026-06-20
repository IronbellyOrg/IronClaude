# Research Notes: Add Layer 5 (H3 subsection-context detector) to obligation_scanner.py

**Date:** 2026-05-29
**Scenario:** A (Explicit — user provided file path, mechanism, mirror pattern, test count, verification approach)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

Files live in the **BareReview worktree** (post-Fix-1/Fix-3 state, not yet committed to master):

- `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli/roadmap/obligation_scanner.py` (710 lines, post-Fix-1+Fix-3)
- `/config/workspace/IronClaude/.claude/worktrees/BareReview/tests/roadmap/test_obligation_scanner.py` (738 lines, has Fix-1/Fix-3 tests)
- `/config/workspace/IronClaude/.claude/worktrees/BareReview/tests/roadmap/test_obligation_scanner_meta_context.py` (394 lines, Layer 3/4 tests)
- `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/releases/Current/MultiModelSwarm/roadmap.md` (e2e smoke roadmap with 8 emergent FPs at lines 145, 149, 278, 425, 437, 474)
- `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/tasks/to-do/TASK-RF-20260529-163344/` (prior task folder with Fix 1 + Fix 3 context)

**Current worktree** (this task's destination): `/config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix/` on branch `worktree-RoadmapCLI-ObligationFix` (fresh from `origin/master`, does NOT have Fix 1/Fix 3 yet).

## PATTERNS_AND_CONVENTIONS

To be discovered by researchers:
- How Layer 4 is wired into the scanner (the layer to mirror)
- How "demote to MEDIUM" is currently implemented
- H3 detection pattern (markdown heading parsing)
- Test fixture conventions in `test_obligation_scanner_meta_context.py`

## GAPS_AND_QUESTIONS

- Does `obligation_scanner.py` already have any H3 tracking, or is this net-new?
- What are the exact H3 strings used in roadmap.md ("Risk Assessment", "Integration Points", "Milestone Dependencies", "Open Questions")?
- What's the milestone boundary marker (H2? specific H2 text pattern)?
- How does the scanner currently determine `current_section`/`current_milestone` state?

## RECOMMENDED_OUTPUTS

Research files (in `${TASK_DIR}research/`):

1. `01-scanner-layer-architecture.md` — Layer 4 implementation details, MEDIUM-demotion pattern, scanner state machine
2. `02-test-conventions.md` — Test patterns in both test files, fixture style, assertion patterns
3. `03-fp-evidence.md` — The 8 emergent FPs: line numbers, surrounding context, H3 subsection each falls under, scaffold terms triggering FP
4. `04-prior-task-context.md` — Read prior TASK-RF-20260529-163344 to extract Fix 1 + Fix 3 lessons, what they fixed, why Layer 5 is emergent (post-Fix)

## SUGGESTED_PHASES

Single track, 4 researchers in parallel:

- **Researcher 1 (File Inventory + Patterns):** Read obligation_scanner.py end-to-end from BareReview worktree. Document: (a) all existing layers (Layer 1..Layer 4), (b) Layer 4's exact wiring — what it detects, how it demotes, where it hooks in, (c) the state-tracking variables (current section/milestone/H3), (d) the demote-to-MEDIUM mechanism's code shape. Output → `01-scanner-layer-architecture.md`. Other researchers cover tests + FP evidence + prior context.

- **Researcher 2 (Test & Verification):** Read both test files from BareReview worktree. Document: (a) fixture patterns (how roadmap text is fed in), (b) assertion patterns (severity, layer, location), (c) how Layer 4 tests are structured (so Layer 5 tests can mirror), (d) the e2e re-verification path — what command/script re-runs the scanner on `.dev/releases/Current/MultiModelSwarm/roadmap.md`. Output → `02-test-conventions.md`.

- **Researcher 3 (FP Evidence):** Read `.dev/releases/Current/MultiModelSwarm/roadmap.md` from BareReview worktree. Extract for EACH of lines 145, 149, 278, 425, 437, 474: (a) the actual line content, (b) the H3 subsection it's under (search backwards for nearest H3), (c) the H2 milestone it's under, (d) the scaffold term triggering the FP. The user said "8 emergent FPs" but listed 6 line numbers — verify which lines map to which FPs. Output → `03-fp-evidence.md`. Other researchers cover scanner code + tests.

- **Researcher 4 (Prior Task Context):** Read prior task folder `TASK-RF-20260529-163344` from BareReview worktree. Document: (a) what Fix 1 was (precise scope), (b) what Fix 3 was (precise scope), (c) what was tested + result counts before/after, (d) why these specific Layer 5 FPs emerged after those fixes — is there a stated reason in the prior task log? Output → `04-prior-task-context.md`.

## TEMPLATE_NOTES

- **Template selection:** 02 (Complex) — discovery (read Layer 4 wiring) → implementation (add Layer 5) → testing (add 3 unit tests) → verification (run e2e). Multi-phase with distinct activities.
- **Tier selection:** Standard — 5-20 file scope is tight (~5 files), but multi-phase with verification gate justifies Standard over Quick.
- **MDTM features:** Per-file granularity (each test is its own item), incremental writing for code edits, e2e re-verification as a measurable gate.
- **Validation:** Standard project — `make lint`, `uv run pytest tests/roadmap/ -v`, plus e2e scanner run on the smoke roadmap.
- **Testing:** UNIT — add 3 new tests to `test_obligation_scanner_meta_context.py` (or new file if pattern dictates).
- **QA gates:** FINAL_ONLY — final phase runs structural QA + e2e re-verification.

## AMBIGUITIES_FOR_USER

1. **Prerequisite branch state:** This worktree is fresh from `origin/master` and does NOT have Fix 1 + Fix 3. The task file's executor will need to either (a) wait for the BareReview branch to merge, OR (b) rebase this branch onto BareReview's branch (`brainstorm/t2-bare-reviewer-adjunct`) before starting. The task file documents this dependency in Prerequisites. **Assumption:** option (b) — rebase onto BareReview's branch — is the intended path since the user spawned a separate worktree expressly to isolate Layer 5 work.

2. **Test file destination:** Should the 3 new Layer 5 tests land in `test_obligation_scanner_meta_context.py` (where Layer 3/4 tests live) or in a new file? **Assumption:** same file (`test_obligation_scanner_meta_context.py`), mirroring Layer 4 placement.

3. **"8 emergent FPs" vs "6 line numbers":** The user said "8 emergent FPs" but provided 6 line numbers (145, 149, 278, 425, 437, 474). Researcher 3 will verify whether two lines each contain two FPs, or the count is approximate.
