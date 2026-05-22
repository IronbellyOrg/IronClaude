# F-28: Stage A stdout-only steps risk disk-Write divergence

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P4, P6
**Identified by**: E-3
**File:line**: `src/superclaude/cli/prd/prompts.py:148-185, 203-260`

## Evidence

```python
# prompts.py:148 -- scope-discovery prompt
OUTPUT FORMAT:
Write a markdown document with these sections:

## Project Overview
[Brief description of what this project is about]
...
```

The prompt says "Write a markdown document" without providing a file path. The intent is stdout, and `_persist_step_artifact` writes the captured stdout to `scope-discovery-raw.md`.

## Trace

- A capable Claude subprocess reading "Write a markdown document" may decide to call the Write tool and put the document on disk at an arbitrary path.
- If that happens, NDJSON stdout contains only commentary like "I've written the scope discovery document to ..." -- and the parent persists that commentary as the artifact.
- Same Bug-1 shape with smaller blast radius (gate `min_lines` for these steps is 50 and 100, which commentary may still clear).

## Reproduction sketch

Run with `--verbose`; inspect `scope-discovery-output.txt` for whether the on-disk artifact contains the full document or "I have written ..." prose.

## Confidence (aggregated)

0.60 -- Agent E flagged as latent behavioral risk, not a confirmed runtime bug. Depends on subprocess's tool-use choices.

## Cross-agent corroboration

- **Agent E** identified the ambiguous prompt wording and traced the consequence if a subprocess chooses to use the Write tool instead of stdout, noting it produces the same Bug-1 shape.
