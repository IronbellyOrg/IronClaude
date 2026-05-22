# F-16: `_resolve_step_content` picks largest file without validation -- cross-run contamination

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P3, P6
**Identified by**: A-11
**File:line**: `src/superclaude/cli/prd/executor.py:279-291`

## Evidence

```python
best_content = ""
for root in search_roots:
    for match in root.rglob(base_name):
        skip_parts = {"node_modules", ".git", "__pycache__"}
        if "-output.txt" in match.name or skip_parts & set(match.parts):
            continue
        try:
            content = match.read_text(encoding="utf-8", errors="replace")
            if len(content) > len(best_content):
                best_content = content
        except OSError:
            continue
```

## Trace

- Searches `task_dir` AND `task_dir.parent` (the project root). For `research-notes.md`, `rglob` from the project root walks the ENTIRE repository.
- If a prior PRD run or an unrelated documentation file named `research-notes.md` exists anywhere under `task_dir.parent` and is larger than the current run's file, it wins.
- No scoping to the current step_id's task_dir, no mtime check, no provenance check.
- Cross-PRD-run contamination is possible.

## Reproduction sketch

Create `/config/workspace/IronClaude/docs/research-notes.md` with 1000 lines of unrelated content, then `superclaude prd run "auth" --product authy`. `_resolve_step_content("research-notes", ...)` picks up the docs file because `task_dir.parent` rglob reaches it.

## Confidence (aggregated)

0.85 -- Agent A verified the code path is direct; severity depends on layout in real directories.

## Cross-agent corroboration

- **Agent A** identified the `rglob` scope issue and the "largest wins" tie-breaking rule, noting that search roots include `task_dir.parent` which can reach any file in the project.
