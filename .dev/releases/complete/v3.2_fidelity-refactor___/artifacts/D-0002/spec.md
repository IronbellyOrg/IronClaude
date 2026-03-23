# D-0002: WiringConfig and Whitelist Loader

- **File**: `src/superclaude/cli/audit/wiring_config.py`
- **WiringConfig**: provider_dir_names (steps, handlers, validators, checks), exclude_patterns, registry_patterns, whitelist_path, rollout_mode
- **load_whitelist()**: shadow mode warns+skips malformed, soft/full raises WiringConfigError
