# D-0087 — NFR-CONV.8 Persistent `.dev/tasks/` Artifact Invariant Audit (T07.05)

**Status:** PASS
**Roadmap Item:** R-144
**Invariant Under Audit:** INV-018 (persistent-`.dev/tasks/`-artifact)
**Source of truth:** release-spec.md §9 SP-33 stability commitment; roadmap-haiku-architect.md:78
**Date:** 2026-05-18
**Auditor:** task-executor (T07.05)

## 1. Scope

NFR-CONV.8 requires that the structural layout of `.dev/tasks/<task-id>/` is unchanged between the pre-merge baseline (`master`) and the post-merge state (current branch `feat/hook-sync-and-matcher-fix`, HEAD = `87c8254`). The contract specifies:

- No new mandatory subdirectory.
- No rename of the canonical subdirectory set (`research`, `qa`, `synthesis`, `reviews`, `adversarial` — the logical contract; the physical-suite name for the adversarial bucket is `phase-outputs/`).
- No change to the `TASK-{TYPE}-YYYYMMDD-...` naming pattern.

The audit captures a pre/post snapshot of the layout, diffs them, and asserts the diff is empty.

## 2. Method

Two snapshots were captured via `git ls-tree -r` (read-only, no working-tree dependency):

| Ref | Commit | Role |
|---|---|---|
| `master` | `516bb46` (merge-base with HEAD) | Pre-merge baseline |
| `HEAD`   | `87c8254` (feat/hook-sync-and-matcher-fix) | Post-merge state |

For each ref the following derived sets were computed:

1. **Bucketed task-directory set** — `.dev/tasks/{done,to-do}/<task-id>/` (top-3 path components).
2. **Canonical subdirectory set** — distinct names of the 4th path component (subdirs immediately under `<task-id>/`).
3. **Task-id naming pattern set** — task-id names with date/track suffixes normalised to `YYYYMMDD-...` / `track-N-...`.
4. **Source-code references** — diff of `.dev/tasks/` mentions in `src/superclaude/skills/**/SKILL.md` and `src/superclaude/agents/`.

All four sets are diffed; INV-018 PASS requires every diff to be empty.

## 3. Snapshots

### 3.1 Canonical subdirectory set (the binding INV-018 surface)

**`master` (pre-merge):**

```
phase-outputs
qa
research
reviews
synthesis
```

**`HEAD` (post-merge):**

```
phase-outputs
qa
research
reviews
synthesis
```

**Diff:** empty. Exit 0.

Note: the contract's logical name `adversarial` is realised on disk as `phase-outputs/` (the rigorflow-suite physical name). This mapping is pre-existing on `master` and unchanged on `HEAD` — no rename has occurred under this release.

### 3.2 Task-id naming-pattern set

**`master` (pre-merge):**

```
TASK-E2E-YYYYMMDD-...
TASK-PRD-YYYYMMDD-...
TASK-RESEARCH-YYYYMMDD-...
TASK-RF-track-N-YYYYMMDD-...
TASK-RF-YYYYMMDD-...
TASK-TDD-YYYYMMDD-...
```

**`HEAD` (post-merge):** identical (byte-equal).

**Diff:** empty. Exit 0.

### 3.3 Top-level bucketed task-directory set

29 task directories present on `master`; 29 task directories present on `HEAD`. `diff` of the full sorted list exits 0. (No tasks added, deleted, renamed, or moved between the two refs.)

### 3.4 Source-code references to `.dev/tasks/`

`git diff master..HEAD -- 'src/superclaude/skills/**/SKILL.md' 'src/superclaude/agents/'` filtered for `.dev/tasks/` references returned zero modifications. The path string, the naming convention, and the subdir contract are not touched by any of MIG-001..MIG-006.

## 4. Acceptance-Criteria Trace

| AC (from phase-7-tasklist.md T07.05) | Result | Evidence |
|---|---|---|
| Diff output between pre-merge and post-merge directory layouts is empty | PASS | §3.1 + §3.3 diffs both exit 0 |
| No new mandatory subdirectory | PASS | §3.1 canonical-subdir sets identical (cardinality 5 → 5) |
| No rename of research/qa/synthesis/reviews/adversarial | PASS | §3.1 — each name appears identically on both refs; `phase-outputs` (physical-name for adversarial) likewise unchanged |
| No naming-pattern change | PASS | §3.2 task-id pattern sets identical |
| INV-018 preservation verified | PASS | §3.4 — zero `.dev/tasks/` source-code reference diffs across MIG-001..MIG-006 |
| Evidence at `TASKLIST_ROOT/artifacts/D-0087/evidence.md` | PASS | this file |

## 5. Verdict

**PASS** — INV-018 / NFR-CONV.8 preserved. K-008 portfolio-wide blast-radius condition is **not** triggered. SP-33 stability commitment holds for the scope of this release.

## 6. Reproduce

```bash
# 1) Capture pre-merge baseline subdir set
git ls-tree -r --name-only $(git merge-base HEAD master) -- .dev/tasks \
  | awk -F/ 'NF>=6 {print $5}' | sort -u > /tmp/inv018/master_subdirs.txt

# 2) Capture post-merge HEAD subdir set
git ls-tree -r --name-only HEAD -- .dev/tasks \
  | awk -F/ 'NF>=6 {print $5}' | sort -u > /tmp/inv018/head_subdirs.txt

# 3) Diff — must exit 0
diff /tmp/inv018/master_subdirs.txt /tmp/inv018/head_subdirs.txt; echo "EXIT=$?"

# 4) Source-code references — must be empty
git diff master..HEAD -- 'src/superclaude/skills/**/SKILL.md' 'src/superclaude/agents/' \
  | grep -E "^[-+].*\.dev/tasks/" | grep -v "^[-+]\{3\}"
```

All four reproduction steps return exit 0 / empty output on commit `87c8254`.
