# D-0016: INTEGRATION_WIRING_DIMENSION in prompts.py

## Status: COMPLETE

## Changes

`src/superclaude/cli/roadmap/prompts.py`:
- `_INTEGRATION_WIRING_DIMENSION` constant added as dimension 6 string
- Instructs LLM to verify wiring tasks for dispatch tables, registries, DI points
- Inserted after dimension 5 (NFRs) in `build_spec_fidelity_prompt()`
- No existing dimensions modified or reordered

## Verification
- `uv run pytest tests/roadmap/ -x` → 1247 passed, 0 failed
