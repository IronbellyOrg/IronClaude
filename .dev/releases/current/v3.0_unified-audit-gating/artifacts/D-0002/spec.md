---
deliverable: D-0002
phase: 2
task: T02.01
status: committed
date: 2026-03-19
---

# D-0002: WiringConfig Dataclass

## Artifact
- `src/superclaude/cli/audit/wiring_config.py`

## Deliverables Implemented
- `WiringConfig` dataclass with `provider_dir_names`, `exclude_patterns`, `registry_patterns`, `whitelist_path`, `rollout_mode`
- `DEFAULT_REGISTRY_PATTERNS` constant (6 compiled regex patterns)
- `load_whitelist()` function with rollout-mode-sensitive error handling (OQ-3)
- `WhitelistEntry` dataclass for typed suppression entries
- `WiringConfigError` exception for strict-mode validation failures

## Acceptance Criteria Met
- Import succeeds: `from superclaude.cli.audit.wiring_config import WiringConfig, DEFAULT_REGISTRY_PATTERNS, load_whitelist`
- Type-checked defaults on all fields
- `load_whitelist()` returns empty list for nonexistent path, populated list for valid YAML
- Rollout mode controls strictness: shadow=warn+skip, soft/full=raise
