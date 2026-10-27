# D-0006 — Evidence

## 1. Workflow diff (the deliverable)

```diff
--- a/.github/workflows/quick-check.yml
+++ b/.github/workflows/quick-check.yml
@@ -43,6 +43,14 @@ jobs:
       - name: Verify pytest plugin
         run: |
           pytest --trace-config 2>&1 | grep -q "superclaude"

+      - name: Verify component sync (src/ ↔ .claude/)
+        run: |
+          make verify-sync
+
+      - name: Lint architecture policy
+        run: |
+          make lint-architecture
+
       - name: Summary
         if: success()
         run: |
@@ -50,3 +58,5 @@ jobs:
           echo "  - Linting: PASSED"
           echo "  - Formatting: PASSED"
           echo "  - Plugin: LOADED"
+          echo "  - Component sync: PASSED"
+          echo "  - Architecture policy: PASSED"
```

GitHub Actions default step semantics (no `continue-on-error`) cause a non-zero exit from either `make verify-sync` or `make lint-architecture` to fail the step → job → workflow.

## 2. Local simulation: probe `.claude/skills/_probe-workspace/` (no SKILL.md)

Setup:
```bash
mkdir -p .claude/skills/_probe-workspace
```

### 2a. `make verify-sync` against probe — fires T02.01 message, exits non-zero

Verbatim line from output:
```
  ❌ _probe-workspace has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/_probe-workspace/.
```

Tail of run:
```
❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
make: *** [Makefile:156: verify-sync] Error 1
EXIT: 2
```

### 2b. `make lint-architecture` against probe — fires T02.02 message, exits non-zero

Captured lines:
```
=== Check 10: Workspace Suffix Blocklist ===
  ❌ ERROR [Check 10]: _probe-workspace — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.
  ❌ FAIL — 4 error(s) found. Fix before proceeding.
EXIT: 2
```

(The "4 errors" total = 3 pre-existing errors + 1 from the probe; see `notes.md`. The probe-attributable error appears verbatim with the FR-L2.3 message.)

Teardown:
```bash
rm -rf .claude/skills/_probe-workspace
```

## 3. Local simulation: clean tree

### 3a. `make verify-sync` clean — exit 0

```
✅ All components in sync.
EXIT: 0
```

### 3b. `make lint-architecture` clean — exits non-zero (pre-existing errors)

3 errors persist independent of any workspace probe:

```
❌ ERROR [Check 1]: src/superclaude/commands/tdd.md has ## Activation but no matching skill directory: sc-tdd-protocol
❌ ERROR [Check 4]: spec-panel.md (651 lines, hard limit 500)
❌ ERROR [Check 6]: task.md missing ## Activation (paired with sc-task-protocol)
EXIT: 2
```

Acceptance Criterion 3 ("a clean PR passes the workflow") is currently **blocked by these 3 pre-existing errors**, not by anything T02.03 introduced. See `notes.md` "Pre-existing lint-architecture errors" for the follow-up plan. The workspace blocklist (Check 10) reports clean on a clean tree:

```
=== Check 10: Workspace Suffix Blocklist ===
  ✅ [Check 10]: no *-workspace directories under .claude/skills/
```

## 4. Mapping to acceptance criteria

| AC | Status | Evidence |
|---|---|---|
| `quick-check.yml` invokes both Makefile targets and fails on non-zero exit | ✅ | §1 diff |
| Synthetic probe shows workflow failure with verbatim T02.01/T02.02 message | ✅ | §2a, §2b |
| Clean PR passes workflow | ⚠ Partial | §3a passes; §3b blocked by 3 pre-existing unrelated errors → see `notes.md` follow-up |
| Failing required check blocks merge OR follow-up note recorded | ✅ (note recorded) | `notes.md` "Branch-protection follow-up" |
| Workflow run URLs / local-act logs captured | ✅ | This file (§2, §3) |

## 5. Synthetic-PR option (deferred)

Live workflow runs were not produced because this environment cannot create PRs against the upstream remote. The `make` invocations above are bit-identical to what the GitHub runner will execute (`run: | make ...`). A reviewer with PR permissions can re-validate end-to-end by:

1. Branching from `master`.
2. `mkdir -p .claude/skills/_probe-workspace && git add -f .claude/skills/_probe-workspace/.gitkeep`.
3. Push, open PR, observe `Quick Test (Python 3.10)` red with the §2a/§2b messages.
