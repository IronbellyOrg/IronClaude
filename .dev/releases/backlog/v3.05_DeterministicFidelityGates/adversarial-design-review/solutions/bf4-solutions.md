# BF-4: Worktree Isolation Doesn't Isolate Input Files

## Bug Summary

Architecture Sec 4.5.1 creates git worktrees for parallel regression validation (FR-8). However, the input files that agents need to read -- `roadmap.md`, `spec-fidelity.md`, `deviation-registry.json` -- live in `output_dir`, which is NOT git-tracked. Git worktrees only isolate git-tracked files. All 3 "isolated" agents would read from the same shared output directory, violating NFR-4 ("Checkers share no mutable state").

---

## Solution A: Copy Artifacts into Each Worktree

### Description

Keep git worktrees for code isolation, but before agent execution, copy the necessary output artifacts into a temporary directory within each worktree. Each agent reads from its local copy.

### Mechanism

```
1. Create 3 git worktrees (as currently designed):
   git worktree add .fidelity-worktree-1 --detach
   git worktree add .fidelity-worktree-2 --detach
   git worktree add .fidelity-worktree-3 --detach

2. For each worktree, create a .fidelity-inputs/ subdirectory:
   .fidelity-worktree-N/.fidelity-inputs/
     roadmap.md              (copied from output_dir)
     spec-fidelity.md        (copied from output_dir)
     deviation-registry.json (copied from output_dir)
     <spec-file>.md          (copied from config.spec_file)

3. Each agent is invoked with input paths pointing to its local copy:
   agent_N reads from .fidelity-worktree-N/.fidelity-inputs/

4. Each agent writes its findings to:
   .fidelity-worktree-N/.fidelity-outputs/findings.json

5. Orchestrator collects findings from all 3 output directories.

6. Cleanup: git worktree remove + rm of temp dirs
```

### Analysis

**True isolation (NFR-4)?** Yes. Each agent has its own copy of all input files. No shared mutable state. Agents also get full repo code if they need to inspect source files referenced in findings.

**Disk space overhead:** HIGH. Each worktree is a full checkout of the repo (working tree, no `.git` duplication thanks to worktree sharing). For a repo with ~50MB working tree, that is ~150MB for 3 worktrees, plus negligible artifact copies (~100KB each).

**Cleanup overhead:** MODERATE. Requires both `git worktree remove` and deletion of the temp input/output directories. Worktree cleanup can fail if processes are still running or if paths are locked.

**Do checkers need the git repo?** NO. The structural checkers (`structural_checkers.py`) operate on parsed `SpecData` and `RoadmapData` from the spec parser. They read exactly 2 files: `spec_path` and `roadmap_path`. They do not import from the repo, run git commands, or inspect source code. The semantic layer similarly receives parsed sections, not repo paths.

**FR-8 alignment:** FULL. FR-8 explicitly states "3 agents spawned in parallel, each in its own git worktree." This solution satisfies the letter of the requirement.

### Pros
- Satisfies FR-8 requirement text exactly (uses git worktrees)
- Provides full repo access if future checkers need source code inspection
- Isolation is guaranteed by filesystem separation

### Cons
- ~150MB disk overhead for 3 full working tree copies
- Worktree lifecycle management adds complexity (creation, cleanup, error handling for orphaned worktrees)
- The git repo is not actually needed by the checkers -- the worktree is wasted overhead
- `git worktree` requires a clean git state; uncommitted changes or locks can cause creation failures

---

## Solution B: Temporary Directory Copies (No Worktrees)

### Description

Abandon git worktrees entirely. Create 3 lightweight temporary directories, copy only the necessary input files into each, and run checkers there. Since the checkers only need spec + roadmap files (not the full git repo), this provides the same isolation with far less overhead.

### Mechanism

```
1. Create 3 temp directories via tempfile.mkdtemp():
   /tmp/fidelity-validation-{uuid}-1/
   /tmp/fidelity-validation-{uuid}-2/
   /tmp/fidelity-validation-{uuid}-3/

2. Copy input files into each:
   /tmp/fidelity-validation-{uuid}-N/
     roadmap.md              (from output_dir)
     spec-fidelity.md        (from output_dir, if exists)
     deviation-registry.json (from output_dir)
     spec.md                 (from config.spec_file)

3. Each agent is invoked with:
   spec_path    = /tmp/.../spec.md
   roadmap_path = /tmp/.../roadmap.md
   registry     = read-only snapshot (not written back per-agent)

4. Each agent writes findings to:
   /tmp/fidelity-validation-{uuid}-N/findings.json

5. Orchestrator collects findings from all 3 temp dirs.

6. Cleanup: shutil.rmtree() on each temp directory.
   Wrapped in try/finally to guarantee cleanup even on exceptions.
```

### Analysis

**True isolation (NFR-4)?** Yes. Each agent operates on its own filesystem copy. No shared paths. No shared mutable state. The frozen dataclass design (SpecData, RoadmapData) already prevents in-memory mutation; this adds filesystem-level isolation on top.

**Disk space overhead:** LOW. Each temp directory contains only 3-4 files totaling ~100-500KB. Total overhead: ~1.5MB for all 3 agents combined, versus ~150MB for worktrees.

**Cleanup overhead:** LOW. `shutil.rmtree()` is a single stdlib call, no git state to manage. Can be wrapped in `atexit` or `try/finally` for guaranteed cleanup. No risk of orphaned worktrees polluting the repo.

**Do checkers need the git repo?** NO. As analyzed above:
- `spec_parser.py` reads 2 files (spec_path, roadmap_path) via `Path.read_text()`.
- `structural_checkers.py` operates on frozen `SpecData`/`RoadmapData` dataclasses -- pure functions.
- `semantic_layer.py` receives parsed sections, not file paths.
- `deviation_registry.py` reads/writes JSON -- no git dependency.
- `convergence.py` orchestrates the above -- no git dependency.
- None of these modules import `git`, run `subprocess` git commands, or need `.git/`.

**FR-8 alignment:** PARTIAL. FR-8 says "each in its own git worktree." This solution does not use git worktrees. However, FR-8's intent is isolation, and the worktree mechanism was chosen under the (incorrect) assumption that it would provide file isolation. Since worktrees don't actually isolate the files that matter, the requirement's implementation strategy is flawed, not its intent.

### Pros
- 100x less disk overhead (~1.5MB vs ~150MB)
- Simpler lifecycle: `mkdtemp` + `rmtree` vs `git worktree add/remove`
- No git state dependencies (no risk of uncommitted changes blocking creation)
- No orphaned worktree risk
- Achieves the actual goal (isolation) directly
- Cleanup is guaranteed via stdlib mechanisms

### Cons
- Does not satisfy FR-8's literal text ("git worktree")
- If future checkers need source code access, temp dirs would need repo files copied too
- Requires updating FR-8 requirement text to reflect the corrected design

---

## Comparison Matrix

| Criterion                     | Weight | Solution A (Worktree + Copy) | Solution B (Temp Dir Only) |
|-------------------------------|--------|------------------------------|---------------------------|
| True isolation (NFR-4)        | 40%    | YES                          | YES                       |
| Disk space efficiency         | 15%    | POOR (~150MB)                | EXCELLENT (~1.5MB)        |
| Cleanup reliability           | 15%    | MODERATE (git state risk)    | HIGH (stdlib rmtree)      |
| Implementation simplicity     | 10%    | MODERATE                     | SIMPLE                    |
| FR-8 literal compliance       | 20%    | FULL                         | PARTIAL (needs FR-8 update) |
| Future extensibility          | 10%    | HIGH (full repo available)   | MODERATE (files only)     |

### Weighted Scores

**Solution A**: (0.40 * 10) + (0.15 * 3) + (0.15 * 6) + (0.10 * 6) + (0.20 * 10) + (0.10 * 9) = 4.0 + 0.45 + 0.9 + 0.6 + 2.0 + 0.9 = **8.85/10**

**Solution B**: (0.40 * 10) + (0.15 * 10) + (0.15 * 10) + (0.10 * 10) + (0.20 * 5) + (0.10 * 6) = 4.0 + 1.5 + 1.5 + 1.0 + 1.0 + 0.6 = **9.60/10**

---

## Recommendation

**Solution B wins.** The decisive factor is that structural checkers do not need the git repo at all. They are pure functions operating on parsed file content. Creating full git worktrees to isolate agents that only need 3-4 files is architectural overengineering. Solution B achieves identical isolation with 100x less disk overhead and simpler lifecycle management.

The FR-8 requirement text should be updated to say "each in its own isolated temporary directory" rather than "each in its own git worktree." The requirement's intent (NFR-4: no shared mutable state) is fully preserved.
