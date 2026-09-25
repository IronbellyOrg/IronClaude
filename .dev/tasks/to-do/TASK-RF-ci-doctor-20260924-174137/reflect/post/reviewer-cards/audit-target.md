# POST audit packet (read-only)

Task: Install native components before CI doctor-check.
Tasklist: TASK-RF-ci-doctor-20260924-174137
Allowed source change: exactly one YAML step in .github/workflows/test.yml doctor-check.

## Diff
```
diff --git a/.github/workflows/test.yml b/.github/workflows/test.yml
@@ -214,6 +214,10 @@ jobs:
         run: |
           uv pip install --system -e ".[dev]"

+      - name: Install native components
+        run: |
+          superclaude install
+
       - name: Run doctor command
         run: |
           superclaude doctor --verbose
```

## Resulting YAML
```
      - name: Install dependencies
        run: |
          uv pip install --system -e ".[dev]"

      - name: Install native components
        run: |
          superclaude install

      - name: Run doctor command
        run: |
          superclaude doctor --verbose
```

## Captured validation
- tests/cli/test_update_command.py: 8 passed EXIT=0
- isolated tmp-HOME: PRE doctor exit 1 (missing ccsession), install exit 0, POST doctor exit 0, CONTRACT=PASS
- git diff --cached --quiet test.yml: 0; workflow.diff equals git diff HEAD; make verify-sync 0
- doctor.py not in the diff

## Taxonomy (required)
Classify each divergence as authorized | necessary | drift | regression.
Expected: YAML hunk is the tasked Step 2.1 (none). Uncommitted delivery, diff-file POST input, and --no-promote are Necessary if they match the task constraints.
Return a deviations table with file:line evidence.
