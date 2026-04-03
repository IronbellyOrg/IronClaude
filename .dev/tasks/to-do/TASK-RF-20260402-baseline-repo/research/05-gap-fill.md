# Research: Gap-Fill — QA Issues Resolution
**Topic type:** Gap-Fill
**Scope:** Resolving 5 QA-identified issues
**Status:** Complete
**Date:** 2026-04-02
---

## Issue #1 (CRITICAL): Anti-Instinct BLOCKING Gate Behavior

### Question
When anti-instinct FAILs, which steps are skipped? What is the realistic artifact count for Test 3?

### Evidence

**Step definition** (`src/superclaude/cli/roadmap/executor.py`, lines 1425-1433):
- `anti-instinct` step has `gate=ANTI_INSTINCT_GATE` with NO explicit `gate_mode` override
- Default is `GateMode.BLOCKING` (from `src/superclaude/cli/pipeline/models.py`, line 89)

**Pipeline halt logic** (`src/superclaude/cli/pipeline/executor.py`, lines 121-122):
```python
if result.status != StepStatus.PASS:
    break
```
When anti-instinct FAILs, the main loop breaks. Test-strategy and spec-fidelity (both BLOCKING, no override) are SKIPPED.

**Deferred trailing steps** (executor.py, lines 124-136):
After the `break`, the pipeline collects any not-yet-executed TRAILING-mode steps and runs them. `wiring-verification` has `gate_mode=GateMode.TRAILING` (executor.py, line 926 on master / line 1464 on feat branch), so it DOES run.

**Confirmed by Test 1 and Test 2 state files:**
Both `.roadmap-state.json` files show exactly 9 steps executed:
1. extract — PASS
2. generate-opus-architect — PASS
3. generate-haiku-architect — PASS
4. diff — PASS
5. debate — PASS
6. score — PASS
7. merge — PASS
8. anti-instinct — **FAIL**
9. wiring-verification — PASS (deferred trailing)

**test-strategy and spec-fidelity are ABSENT** from both state files — they never ran.

**Same behavior on master** (commit 4e0c621): Verified identical logic in `git show master:src/superclaude/cli/pipeline/executor.py` and `git show master:src/superclaude/cli/roadmap/executor.py`.

### Finding
**Realistic artifact count for Test 3: 9 content files**, not 11. The pipeline will produce:
1. extraction.md
2. roadmap-opus-architect.md
3. roadmap-haiku-architect.md
4. diff-analysis.md
5. debate-transcript.md
6. base-selection.md
7. roadmap.md
8. anti-instinct-audit.md
9. wiring-verification.md

test-strategy.md and spec-fidelity.md will NOT be produced.

---

## Issue #2 (CRITICAL): .dev/ and docs/generated/ Git Tracking Status

### Question
Is `.dev/` gitignored? Does it exist on master?

### Evidence

**`git check-ignore .dev/`** returned exit code 1 (NOT ignored).

**`.gitignore`** contains NO pattern matching `.dev/` or `.dev`. (Full .gitignore reviewed — no relevant exclusion.)

**`git ls-tree master .dev/`** shows `.dev/` IS tracked on master with these subdirectories:
- `.dev/benchmarks`
- `.dev/releases`
- `.dev/research`
- `.dev/tasks`
- `.dev/test-sprints`

**`git ls-tree master .dev/test-fixtures/`** returned EMPTY — `.dev/test-fixtures/` does NOT exist on master.

### Finding
- `.dev/` is **tracked in git, NOT gitignored**. The worktree researcher was WRONG.
- `.dev/test-fixtures/` does NOT exist on master — it must be created in the worktree.
- A worktree based on master will have `.dev/` with benchmarks, releases, research, tasks, test-sprints but NOT test-fixtures.
- The task must create `.dev/test-fixtures/` and copy the spec fixture into it.

---

## Issue #3 (IMPORTANT): Actual File Count in Test 2 Output

### Question
Is the file count 18 (9 content + 9 .err), 16 (9 .md + 7 .err), or something else?

### Evidence

**`ls -la .dev/test-fixtures/results/test2-spec-modified/`** shows exactly 19 entries (including `.` and `..`), meaning **17 files** plus `.roadmap-state.json`:

Content files (9 .md):
1. anti-instinct-audit.md (1,013 bytes)
2. base-selection.md (10,431 bytes)
3. debate-transcript.md (23,072 bytes)
4. diff-analysis.md (12,674 bytes)
5. extraction.md (17,129 bytes)
6. roadmap-haiku-architect.md (26,041 bytes)
7. roadmap-opus-architect.md (21,216 bytes)
8. roadmap.md (31,096 bytes)
9. wiring-verification.md (3,064 bytes)

Error files (7 .err, ALL zero-byte):
1. base-selection.err (0 bytes)
2. debate-transcript.err (0 bytes)
3. diff-analysis.err (0 bytes)
4. extraction.err (0 bytes)
5. roadmap-haiku-architect.err (0 bytes)
6. roadmap-opus-architect.err (0 bytes)
7. roadmap.err (0 bytes)

State file (1):
1. .roadmap-state.json (3,228 bytes)

### Finding
**Actual count: 9 .md + 7 .err + 1 .roadmap-state.json = 17 files total**.

Two .md files have NO corresponding .err file:
- `anti-instinct-audit.md` — deterministic (non-LLM) step, no subprocess, no .err
- `wiring-verification.md` — deterministic (non-LLM) step, no subprocess, no .err

Both the "18 files" claim and the "16 files" claim were wrong. The accurate count is **17 files** (or 16 excluding state file, or 9 content + 7 .err = 16 excluding state).

QA was closer: 9 .md + 7 .err = 16 artifact files + 1 state file.

---

## Issue #4 (IMPORTANT): Realistic Artifact Expectations for Comparison

### Question
What should Test 2 vs Test 3 comparison actually cover?

### Evidence

**Both Test 1 and Test 2** show identical step execution patterns:
- 7 LLM steps PASS (extract through merge)
- anti-instinct FAIL (deterministic)
- wiring-verification PASS (deferred trailing, deterministic)
- test-strategy NEVER RAN
- spec-fidelity NEVER RAN

**Test 3 (baseline master, commit 4e0c621)** will use the same pipeline logic (verified above), so the same 9 steps will execute. Anti-instinct will almost certainly FAIL again (it checks spec obligations against the merged roadmap — this is content-dependent but structurally tends to fail).

### Finding

**Realistic comparison between Test 2 and Test 3:**

Both will produce the same 9 artifacts. The comparison should focus on:

1. **LLM-generated artifacts (7 files)** — these WILL differ because:
   - Test 2 uses the MODIFIED spec (fidelity prompt added at top)
   - Test 3 uses the ORIGINAL spec (no fidelity prompt)
   - The "fidelity prompt language" is the ONE expected difference in input
   - Output differences should be traced to whether the fidelity prompt influences roadmap quality

2. **Deterministic artifacts (2 files)** — these MAY differ because:
   - anti-instinct-audit.md depends on spec content AND merged roadmap content
   - wiring-verification.md runs static analysis on `src/superclaude/` — should be identical if same codebase

3. **Artifacts that will NOT exist in either test:**
   - test-strategy.md — pipeline halts before it
   - spec-fidelity.md — pipeline halts before it

**Key correction:** The task's comparison criteria should NOT expect test-strategy or spec-fidelity artifacts in either Test 2 or Test 3.

---

## Issue #5 (MINOR): Placeholder Filename

### Finding
The worktree researcher used `<spec-fixture>.md` as a placeholder. The correct filename is `test-spec-user-auth.md`, as confirmed by:
- Test 2 `.roadmap-state.json` `spec_file` field: `.dev/test-fixtures/test-spec-user-auth.md`
- This file must be copied into the worktree's `.dev/test-fixtures/` directory for Test 3.

---

## Summary of Corrected Facts

| Item | Previous Claim | Corrected Fact |
|------|---------------|----------------|
| Anti-instinct gate mode | "BLOCKING gate" (correct but incomplete) | BLOCKING gate; pipeline halts but wiring-verification still runs as deferred TRAILING step |
| Realistic artifact count | "9 artifacts" or "11 artifacts" | **9 content artifacts** (7 LLM + 2 deterministic); test-strategy and spec-fidelity are SKIPPED |
| .dev/ gitignored? | "almost certainly gitignored" | **NOT gitignored, IS tracked on master** |
| .dev/test-fixtures/ on master? | Unknown | **Does NOT exist on master** — must be created |
| Test 2 file count | "18 files" or "16 files" | **17 files**: 9 .md + 7 .err (zero-byte) + 1 .roadmap-state.json |
| Comparison scope | "fidelity prompt is ONE expected difference" | Correct for inputs, but neither test will have test-strategy/spec-fidelity output |
| Spec fixture filename | `<spec-fixture>.md` | `test-spec-user-auth.md` |

### Impact on Task File

The task file for E2E Test 3 must:
1. Set expected artifact count to **9** (not 11)
2. Create `.dev/test-fixtures/` in the worktree (it doesn't exist on master)
3. Expect comparison of 9 matching artifacts between Test 2 and Test 3
4. NOT expect test-strategy.md or spec-fidelity.md in either test's output
5. Use filename `test-spec-user-auth.md` for the spec fixture
