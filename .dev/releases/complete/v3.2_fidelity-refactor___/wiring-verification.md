---
gate: wiring-verification
target_dir: /config/workspace/IronClaude/.dev/releases/current
files_analyzed: 0
files_skipped: 0
rollout_mode: soft
analysis_complete: true
audit_artifacts_used: 0
unwired_callable_count: 0
orphan_module_count: 0
unwired_registry_count: 0
critical_count: 0
major_count: 0
info_count: 0
total_findings: 0
blocking_findings: 0
whitelist_entries_applied: 0
---

## Summary

- **Target**: /config/workspace/IronClaude/.dev/releases/current
- **Files analyzed**: 0
- **Files skipped**: 0
- **Rollout mode**: soft
- **Total findings**: 0
- **Blocking findings**: 0
- **Scan duration**: 0.0035s

## Unwired Optional Callable Injections

No unsuppressed unwired callable findings.

## Orphan Modules / Symbols

No unsuppressed orphan module findings.

## Unregistered Dispatch Entries

No unsuppressed registry findings.

## Suppressions and Dynamic Retention

No suppressions applied.

- Audit artifacts used: 0

## Recommended Remediation

No remediation needed — all checks pass.

## Evidence and Limitations

- Analysis uses AST-based static analysis; dynamic imports and runtime wiring are not detected.
- Alias resolution is limited to direct name references.
- Registry detection uses pattern matching on variable names; non-conventional naming may be missed.
