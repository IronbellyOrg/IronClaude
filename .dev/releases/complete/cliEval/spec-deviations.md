---
schema_version: 1
total_analyzed: 20
unclassified_count: 0
no_action_count: 20
routing_fix_roadmap: 
routing_no_action: all-20-deviations
analysis_complete: true
manual_triage_applied: 2026-05-19
manual_triage_source: deviation-triage.md
manual_triage_decision: decisions.md#D-9
---

> NOTE: deviation classification is not yet implemented in the pipeline. All 20 records were originally UNCLASSIFIED. Per `decisions.md#D-9` manual-triage policy, a maintainer reviewed each finding against `roadmap.md` and `decisions.md`; all 20 were resolved as `NO_ACTION` (analyzer false-positives). See `deviation-triage.md` for per-deviation evidence and root-cause analysis. Re-run will auto-resolve once the classifier (backlog item `pipeline-classifier-implementation`) is implemented.

# Deviation Analysis Report

Total deviations analyzed: 20
- No-action (manual triage, analyzer false-positives): 20

## Deviation Details

### 6066cc29f9e8e271 [NO_ACTION]
- Description: File 'src/superclaude/cli/install_hooks.py:install_hooks' in spec manifest not found in roadmap
- Location: spec:file:src/superclaude/cli/install_hooks.py:install_hooks

### 4fb19958cd68ccd5 [NO_ACTION]
- Description: File 'src/superclaude/hooks/hooks.json' in spec manifest not found in roadmap
- Location: spec:file:src/superclaude/hooks/hooks.json

### 6205bc801751e4ee [NO_ACTION]
- Description: File 'tests/cli/test_eval/test_pty_vendor.py' in spec manifest not found in roadmap
- Location: spec:file:tests/cli/test_eval/test_pty_vendor.py

### 4a593f91fa2f71ce [NO_ACTION]
- Description: File 'tests/cli/test_install_hooks.py' in spec manifest not found in roadmap
- Location: spec:file:tests/cli/test_install_hooks.py

### f009208dd67590eb [NO_ACTION]
- Description: Function 'contains_event' defined in spec not found in roadmap
- Location: spec:function:contains_event

### f877a1203015d2c0 [NO_ACTION]
- Description: Function 'does_not_contain' defined in spec not found in roadmap
- Location: spec:function:does_not_contain

### 810eecb0074c0e0e [NO_ACTION]
- Description: Function 'event_count' defined in spec not found in roadmap
- Location: spec:function:event_count

### 554f05e7b982946b [NO_ACTION]
- Description: Function 'greater_than' defined in spec not found in roadmap
- Location: spec:function:greater_than

### 66492521b8818cdf [NO_ACTION]
- Description: Function 'has_content_matching' defined in spec not found in roadmap
- Location: spec:function:has_content_matching

### 036e07b465bba3be [NO_ACTION]
- Description: Function 'has_mode' defined in spec not found in roadmap
- Location: spec:function:has_mode

### ca8f41af98446948 [NO_ACTION]
- Description: Function 'has_registration' defined in spec not found in roadmap
- Location: spec:function:has_registration

### 79499bd34957b279 [NO_ACTION]
- Description: Function 'hooks_count' defined in spec not found in roadmap
- Location: spec:function:hooks_count

### 7f2eecdaf000a2ac [NO_ACTION]
- Description: Function 'is_valid_jsonl' defined in spec not found in roadmap
- Location: spec:function:is_valid_jsonl

### 7af318d32b4c43e7 [NO_ACTION]
- Description: Function 'less_than' defined in spec not found in roadmap
- Location: spec:function:less_than

### e300bee8d19358c4 [NO_ACTION]
- Description: Function 'matches_line' defined in spec not found in roadmap
- Location: spec:function:matches_line

### b3e986e55a453d79 [NO_ACTION]
- Description: Roadmap references ID 'D-1' not found in spec
- Location: roadmap:D-1

### aafa5eb94a0deb89 [NO_ACTION]
- Description: Roadmap references ID 'D12' not found in spec
- Location: roadmap:D12

### ebc2911b1f8da5a2 [NO_ACTION]
- Description: Roadmap references ID 'D3' not found in spec
- Location: roadmap:D3

### 9e340eb20538b876 [NO_ACTION]
- Description: Roadmap references ID 'D5' not found in spec
- Location: roadmap:D5

### 44e2b33673c030ef [NO_ACTION]
- Description: Roadmap references ID 'D6' not found in spec
- Location: roadmap:D6
