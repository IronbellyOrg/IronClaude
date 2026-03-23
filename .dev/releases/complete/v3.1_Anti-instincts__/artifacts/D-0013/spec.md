# D-0013: _run_anti_instinct_audit() Function

## Status: COMPLETE

## Changes

`src/superclaude/cli/roadmap/executor.py`:
- `_run_anti_instinct_audit(spec_file, roadmap_file, output_file)` — deterministic (no LLM)
- Reads spec + merged roadmap, invokes all three detection modules:
  - `scan_obligations()` from obligation_scanner
  - `extract_integration_contracts()` + `check_roadmap_coverage()` from integration_contracts
  - `check_fingerprint_coverage()` from fingerprint
- Writes `anti-instinct-audit.md` with YAML frontmatter containing:
  `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
- Anti-instinct step handled in `roadmap_run_step()` directly (no Claude subprocess)
- `_run_structural_audit()` warning-only hook added after EXTRACT_GATE pass

## Verification
- `uv run pytest tests/roadmap/ -x` → 1247 passed, 0 failed
