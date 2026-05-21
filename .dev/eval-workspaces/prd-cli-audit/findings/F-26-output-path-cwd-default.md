# F-26: `output_path` default resolves `.dev/eval-workspaces` at CWD without verifying project root

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P5, P7
**Identified by**: C-9
**File:line**: `src/superclaude/cli/prd/config.py:108-117`

## Evidence

```python
sandbox = Path(".dev/eval-workspaces").resolve()
if sandbox.parent.is_dir():            # i.e. .dev/ exists as a dir
    sandbox.mkdir(parents=True, exist_ok=True)
    output_path = sandbox
```

## Trace

- The CWD-relative `.dev/eval-workspaces` triggers whenever any `.dev/` directory exists in CWD.
- If the user is in a subdirectory or an unrelated project that happens to have a `.dev/` directory, the PRD pipeline writes outside what the user expected and never asks permission.
- Compounded by F-14: `output_path` is treated as a directory parent. So the pipeline silently creates `<cwd>/.dev/eval-workspaces/prd-<slug>/` without advisory in dry-run output.

## Reproduction sketch

From any CWD containing a `.dev/` directory: `superclaude prd run "x"` silently creates `<cwd>/.dev/eval-workspaces/prd-task/`.

## Confidence (aggregated)

0.85 -- Agent C verified the behavior; severity depends on house convention.

## Cross-agent corroboration

- **Agent C** identified the CWD-relative resolution and the lack of project-root verification, noting that the convention is not unique to this repo and could trigger in unrelated projects.
