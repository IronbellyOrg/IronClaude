# Research Notes — TASK-RF-track-1 (FU-001: sprint runner .sprint-exitcode writes to tracked path)

**Scenario:** A (Explicit — stubs gave hypotheses, references, acceptance criteria)
**Depth Tier:** Standard
**Track Count:** 3 of 3 (multi-track build)
**Template:** 02 (Complex — discovery + fix + test + validation phases)

---

## GOAL

Migrate sprint runner's `.sprint-exitcode` writes from the tracked release archive path (`config.release_dir`) to a non-tracked transient state directory. Remove 40 tracked `.sprint-exitcode` files (via `git rm --cached`) and add the new transient location to `.gitignore`.

## WHY

~40 tracked `.sprint-exitcode` files exist under `.dev/releases/**/` from historical writes. These are transient runner exitcode markers that conflate runtime state with archive. The Phase 3 `.gitignore` anchoring to `/` only was a workaround; the root fix is moving the writer.

---

## 1. EXISTING_FILES

- `src/superclaude/cli/sprint/executor.py:1714` — writes `(config.release_dir / ".sprint-exitcode").write_text(str(_exitcode))`
- `src/superclaude/cli/sprint/tmux.py:166` — references `config.release_dir / ".sprint-exitcode"` (read or write?)
- `src/superclaude/cli/sprint/config.py` — defines `release_dir` and `SprintConfig` model (needs new `state_dir` field)
- `src/superclaude/cli/sprint/models.py` — `SprintConfig` / `Phase` models
- 19 total `.py` files in `src/superclaude/cli/sprint/`
- Existing tracked `.sprint-exitcode` files: 40 under `.dev/releases/**/`
- Reference stub: `.dev/tasks/to-do/follow-ups/FU-001-tasklist-root-manifest-bug.md`
- Parent task QA report: `.dev/tasks/to-do/TASK-RF-20260518-181333/qa/qa-phase-3-report.md`
- `.gitignore` patterns from cleanup commit `fe11bd8` (anchored `/.sprint-exitcode`)

## 2. PATTERNS_AND_CONVENTIONS

- Config field naming: snake_case Path attrs on `SprintConfig` (e.g., `release_dir`)
- New env var convention: `SPRINT_STATE_DIR` or constructor param
- Tests live in `tests/sprint/` (existing tests confirmed via PR-A: 1350 tests pass on the C1-C4 fixed code)

## 3. GAPS_AND_QUESTIONS

- Should existing 40 tracked files be (a) `git rm --cached`-only (leave on disk) or (b) deleted entirely? Stub says "preserved or moved"; researcher must inventory whether they have content or are 0-byte markers.
- Where exactly does `release_dir` get set in `SprintConfig`? (config.py loader)
- Does `tmux.py` read or write `.sprint-exitcode`? (impacts whether tmux also needs the new path)
- Are there other internal sprint writers of `.sprint-exitcode` that the grep missed (e.g., in tests, fixtures)?
- Should the new `state_dir` be `.dev/sprint-state/<tasklist-id>/` or `/tmp/sprint-state/<tasklist-id>/`?

## 4. RECOMMENDED_OUTPUTS

3 researchers:

- `research/01-file-inventory.md` — every `sprint/*.py` reference to `release_dir`, exit-code writes, tmux read sites
- `research/02-config-pattern.md` — how `SprintConfig` is constructed (`config.py` + `models.py`), where `release_dir` defaults, how a new `state_dir` field would compose
- `research/03-template-examples.md` — read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 fully + check 1-2 done/ tasks under `.dev/tasks/done/` that touched sprint config (if any)

## 5. SUGGESTED_PHASES

1. Audit + Inventory phase (locate all 40 tracked files; identify tmux/executor/test writers)
2. Add `SPRINT_STATE_DIR` + `state_dir` field phase (`config.py` + `models.py`)
3. Migrate writers phase (`executor.py:1714`, `tmux.py:166`)
4. Remove from tracking phase (`git rm --cached` for 40 files; gitignore update)
5. Test phase (sprint test suite must remain green)
6. Validation phase (lint + verify-sync + `git ls-files` check)
7. Completion phase

## 6. TEMPLATE_NOTES

Template 02 (Complex). Includes discovery phase, refactor across multiple modules, test/validation phases. Tier: Standard.

## 7. AMBIGUITIES_FOR_USER

- Disposition of 40 existing tracked files (keep historical or rewrite history)
- Choice of state-dir location (`.dev/sprint-state/` vs `/tmp/`)
