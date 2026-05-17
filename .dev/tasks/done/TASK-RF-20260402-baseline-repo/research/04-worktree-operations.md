# Research: Git Worktree & Cross-Repo Operations for E2E Test 3

- **Researcher**: researcher-worktree-ops
- **Date**: 2026-04-02
- **Status**: Complete
- **Scope**: Exact workflow for creating, using, and cleaning up a git worktree from master to run the baseline `superclaude roadmap run` pipeline

---

## 1. Current State

### Worktree Status
```
$ git worktree list
/Users/cmerritt/GFxAI/IronClaude  b942d50 [feat/tdd-spec-merge]
```
- Only the main working tree exists
- No existing worktree at `../IronClaude-baseline`
- No cleanup needed before starting

### Master Branch
- Master is at commit `4e0c621` (Merge PR #19: v3.7-TurnLedgerWiring)
- Master has: `superclaude roadmap run` command, `make install` target, full CLI entry points

---

## 2. Key Finding: No `make dev` Target

The CLAUDE.md references `make dev`, but **the actual Makefile has `make install`**, not `make dev`. The target:

```makefile
install:
	uv pip install -e ".[dev]"
```

This is the equivalent of what `make dev` is described as. The E2E test must use `make install`, not `make dev`. This applies to both the current Makefile and the master branch Makefile (verified via `git show master:Makefile`).

---

## 3. Complete Worktree Workflow (Exact Commands)

### Step 1: Create the Worktree

```bash
cd /Users/cmerritt/GFxAI/IronClaude
git worktree add ../IronClaude-baseline master
```

**What this does:**
- Creates `/Users/cmerritt/GFxAI/IronClaude-baseline/` as a new working directory
- Checks out the `master` branch there
- The worktree shares `.git` internals with the main repo (via a `.git` file, not directory)
- The main repo remains on `feat/tdd-spec-merge`

**Constraint:** The `master` branch cannot be checked out in the main repo while the worktree exists. This is fine since the main repo is on a feature branch.

### Step 2: Install the Baseline Package

```bash
cd /Users/cmerritt/GFxAI/IronClaude-baseline
make install
```

This runs `uv pip install -e ".[dev]"` in the worktree. 

**GOTCHA -- Virtual Environment Isolation:**
- If the main repo and worktree share the same virtualenv (e.g., the project uses a `.venv` at the repo root), `make install` in the worktree will overwrite the editable install to point at the worktree's source.
- UV typically creates a `.venv` in the project root. Since the worktree is at a different path (`../IronClaude-baseline/`), UV should create a separate `.venv` there.
- **Verify after install:** `uv run superclaude --version` should work in the worktree.
- After cleanup, you may need to re-run `make install` in the main repo to restore the editable install.

### Step 3: Create Required Directories and Copy Spec Fixture

```bash
# Create the fixture directory in the worktree
mkdir -p /Users/cmerritt/GFxAI/IronClaude-baseline/.dev/test-fixtures/

# Copy the spec fixture from the main repo into the worktree
# (The spec fixture path will be determined by researcher-file-inventory)
cp /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/<spec-fixture>.md \
   /Users/cmerritt/GFxAI/IronClaude-baseline/.dev/test-fixtures/
```

**Note:** The `.dev/` directory is likely gitignored, so it won't exist in the worktree after checkout. It must be created explicitly.

**Also needed:**
```bash
# Create output directory for roadmap artifacts
mkdir -p /Users/cmerritt/GFxAI/IronClaude-baseline/docs/generated/
```

### Step 4: Run the Pipeline in the Worktree

```bash
cd /Users/cmerritt/GFxAI/IronClaude-baseline
uv run superclaude roadmap run .dev/test-fixtures/<spec-fixture>.md \
    --output docs/generated/baseline-output/
```

**Alternative if --output is not used:** The roadmap command defaults output to the parent directory of the spec file, so artifacts would land in `.dev/test-fixtures/`.

### Step 5: Copy Results Back to Main Repo

```bash
# Copy the baseline output back to the main repo's test artifacts area
cp -r /Users/cmerritt/GFxAI/IronClaude-baseline/docs/generated/baseline-output/ \
      /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/baseline-output/
```

**Alternatively**, the E2E test script can read directly from the worktree path before cleanup.

### Step 6: Clean Up the Worktree

```bash
cd /Users/cmerritt/GFxAI/IronClaude
git worktree remove ../IronClaude-baseline
```

If there are untracked files (which there will be, since `.dev/` and `docs/generated/` were created), use:

```bash
git worktree remove --force ../IronClaude-baseline
```

**Post-cleanup:** Optionally re-run `make install` in the main repo if the virtualenv was affected.

---

## 4. Gotchas and Edge Cases

### 4.1 Shared .git Internals
- Worktrees share the same `.git` object store via a pointer file (`.git` in the worktree is a file, not a directory, containing `gitdir: /Users/cmerritt/GFxAI/IronClaude/.git/worktrees/IronClaude-baseline`)
- **Impact:** Git operations in one tree are visible to the other (e.g., creating a commit on master in the worktree will move master's HEAD for both)
- **Mitigation:** Don't commit in the worktree; it's read-only for test purposes

### 4.2 Lock Files
- Git creates a lock file at `.git/worktrees/IronClaude-baseline/locked` if the worktree is locked
- If a previous worktree remove failed, stale lock files may remain
- **Fix:** `git worktree prune` clears stale entries

### 4.3 UV / Python Environment Isolation
- UV creates `.venv` per-project-root by default
- The worktree at `../IronClaude-baseline/` will get its own `.venv` since it's a different directory with its own `pyproject.toml`
- **However:** If `UV_PROJECT_ENVIRONMENT` is set globally, both trees could share an env -- check before running
- **Safest approach:** Explicitly create a venv: `cd /path/to/worktree && uv venv && make install`

### 4.4 .gitignore and Missing Directories
- `.dev/` is almost certainly gitignored (it contains task/fixture data, not tracked code)
- `docs/generated/` may also be gitignored
- These directories will NOT exist in a fresh worktree checkout -- must be created manually

### 4.5 Branch Locking
- While the worktree exists, `master` cannot be checked out in the main repo
- `git branch -d master` will also fail
- This is fine for E2E test purposes but the test must clean up the worktree to avoid blocking other workflows

### 4.6 Concurrent Operations
- Running `superclaude roadmap run` in the worktree while another instance runs in the main repo is safe as long as they write to different output directories
- The shared `.git` means `git status` may show unexpected output if both trees are modified simultaneously

---

## 5. Recommended E2E Test Script Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

MAIN_REPO="/Users/cmerritt/GFxAI/IronClaude"
WORKTREE_PATH="${MAIN_REPO}/../IronClaude-baseline"
SPEC_FIXTURE="<spec-fixture>.md"  # Set by researcher-file-inventory
BASELINE_OUTPUT="baseline-output"

# --- Setup ---
cd "$MAIN_REPO"

# Clean up any stale worktree
git worktree prune

# Create worktree from master
git worktree add "$WORKTREE_PATH" master

# Install in worktree
cd "$WORKTREE_PATH"
uv venv          # Explicit venv creation for isolation
make install

# Prepare fixture directories
mkdir -p .dev/test-fixtures/ docs/generated/

# Copy spec fixture from main repo
cp "${MAIN_REPO}/.dev/test-fixtures/${SPEC_FIXTURE}" .dev/test-fixtures/

# --- Run Baseline Pipeline ---
uv run superclaude roadmap run ".dev/test-fixtures/${SPEC_FIXTURE}" \
    --output "docs/generated/${BASELINE_OUTPUT}/"

# --- Collect Results ---
mkdir -p "${MAIN_REPO}/.dev/test-fixtures/${BASELINE_OUTPUT}/"
cp -r "docs/generated/${BASELINE_OUTPUT}/"* \
      "${MAIN_REPO}/.dev/test-fixtures/${BASELINE_OUTPUT}/"

# --- Cleanup ---
cd "$MAIN_REPO"
git worktree remove --force "$WORKTREE_PATH"

echo "Baseline artifacts available at: .dev/test-fixtures/${BASELINE_OUTPUT}/"
```

---

## 6. Verification Checklist for Task File

| Item | Verified | Notes |
|------|----------|-------|
| `git worktree add ../IronClaude-baseline master` works | Yes | No existing worktree conflicts; master branch available |
| Makefile target is `make install` (not `make dev`) | Yes | Both current and master Makefile use `install:` target with `uv pip install -e ".[dev]"` |
| `superclaude roadmap run` exists on master | Yes | Verified via `git show master:src/superclaude/cli/roadmap/commands.py` |
| CLI entry point `superclaude` on master | Yes | `pyproject.toml` has `superclaude = "superclaude.cli.main:main"` |
| `.dev/` directory needs manual creation | Yes | Almost certainly gitignored |
| `git worktree remove --force` needed for cleanup | Yes | Untracked files in `.dev/` and `docs/generated/` require `--force` |
| Environment isolation with UV | Caution | Recommend explicit `uv venv` in worktree before `make install` |
| Re-install in main repo after cleanup | Maybe | Only if editable install paths got confused; test and verify |

---

## 7. Summary for Task Builder

**Use `make install`** (not `make dev`) -- both the CLAUDE.md and actual Makefile diverge on naming.

**Critical path:** worktree create -> uv venv -> make install -> mkdir fixtures -> cp spec -> run pipeline -> cp results -> worktree remove --force

**Key risks:** UV environment cross-contamination (mitigated by explicit `uv venv`), missing `.dev/` directory (mitigated by explicit `mkdir -p`), stale worktree locks (mitigated by `git worktree prune` at start).
