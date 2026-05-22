# F-14: `output_path` file-vs-directory pun -- CLI treats as dir, prompts present as file

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P5, P7
**Identified by**: C-4
**File:line**: `src/superclaude/cli/prd/config.py:102-117, 125`; `src/superclaude/cli/prd/models.py:184`; `src/superclaude/cli/prd/prompts.py:919, 1093, 986, 1042`

## Evidence

```python
# config.py:103 -- always resolves to a directory
if output:
    output_path = Path(output).resolve()
else:
    sandbox = Path(".dev/eval-workspaces").resolve()
    ...
    output_path = sandbox          # always a directory

# config.py:125 -- treats as parent dir
task_dir = output_path / task_dir_name  # mkdir under it

# prompts.py:919 -- presents to LLM as final file
Output path: {config.output_path}
# prompts.py:1093
Final PRD: {config.output_path}
```

## Trace

- **Writer**: `--output` -> `Path(output).resolve()` with no isfile/isdir check. Default branch hard-codes `.dev/eval-workspaces/` (a directory).
- **Reader A** (config.py:125): `task_dir = output_path / task_dir_name` -- treats it as a directory parent.
- **Reader B** (prompts.py:919, 986, 1042, 1093): renders into prompts as a single path the LLM is told to "Write to" or "Report path".
- **Chain break**: If user passes `--output ./out.md`, executor does `mkdir -p ./out.md/prd-<slug>/...`, creating a directory named `out.md`. The LLM sees a directory path where the prompt says "Final PRD:".

## Reproduction sketch

`superclaude prd run "x" --output prd.md --product foo --dry-run` prints `Output: /.../prd.md`. A non-dry run would `mkdir prd.md/prd-foo/...` -- a directory named `prd.md`.

## Confidence (aggregated)

0.90 -- Agent C verified all code paths. The pun (writer treats as dir, prompt label treats as file) is fully evidenced.

## Cross-agent corroboration

- **Agent C** traced the full ambiguity: the CLI help says "Output path for final PRD" (implies file), but `config.py` always uses it as a directory parent for `task_dir`, while prompts present it to the LLM as a file path.
