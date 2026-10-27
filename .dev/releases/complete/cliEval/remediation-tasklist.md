---
type: remediation-tasklist
source_report: /config/workspace/IronClaude/.dev/releases/current/cliEval/spec-fidelity.md
source_report_hash: 5f483d2046ba46a65de69cda6bfa99f278198d50f8c6a8ee9d7e2605577bf2c2
generated: 2026-05-18T19:41:57.687851+00:00
triage_applied: 2026-05-19
triage_source: deviation-triage.md
triage_decision: decisions.md#D-9
total_findings: 20
actionable: 20
skipped: 0
resolved_no_action: 20
resolved_mapped: 0
escalated: 0
---

# Remediation Tasklist

All 20 BLOCKING entries were triaged per `decisions.md#D-9` manual-triage policy and resolved as `NO_ACTION` (analyzer false-positives). See `deviation-triage.md` for full per-deviation evidence and root-cause analysis. None of the original 20 represent real spec↔roadmap gaps.

## BLOCKING

- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- File 'src/superclaude/cli/install_hooks.py:install_hooks' in spec manifest not found in roadmap | Evidence: roadmap.md:102,142,409 (HARD reuse anchor + COMP-014 deliverable)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- File 'src/superclaude/hooks/hooks.json' in spec manifest not found in roadmap | Evidence: roadmap.md:142,410 (COMP-014 deliverable + HARD reuse anchor)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- File 'tests/cli/test_eval/test_pty_vendor.py' in spec manifest not found in roadmap | Evidence: roadmap.md:412 (HARD reuse anchor, gates vendored ptytest)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- File 'tests/cli/test_install_hooks.py' in spec manifest not found in roadmap | Evidence: roadmap.md:411 (HARD reuse anchor, gates COMP-014)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'contains_event' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'does_not_contain' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'event_count' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'greater_than' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'has_content_matching' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'has_mode' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'has_registration' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'hooks_count' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'is_valid_jsonl' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'less_than' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Function 'matches_line' defined in spec not found in roadmap | Evidence: roadmap.md:77 (COMP-010 ExpectDSL predicate helper)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Roadmap references ID 'D-1' not found in spec | Evidence: grep '\bD-1\b' roadmap.md returns 0 matches; phantom extraction (only D-5,D-8 exist at roadmap.md:57,86,109,344,348)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Roadmap references ID 'D12' not found in spec | Evidence: grep '\bD12\b' roadmap.md returns 0 matches; phantom extraction (D12 does not exist in any cliEval artifact)
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Roadmap references ID 'D3' not found in spec | Evidence: grep '\bD3\b' roadmap.md returns 0 matches; phantom extraction
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Roadmap references ID 'D5' not found in spec | Evidence: grep '\bD5\b' roadmap.md returns 0 matches; only hyphenated D-5 (ADR label) appears at roadmap.md:57,86,109,344,348
- [x] RyanW | /config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md | RESOLVED → NO_ACTION (analyzer false-positive, see deviation-triage.md) -- Roadmap references ID 'D6' not found in spec | Evidence: grep '\bD6\b' roadmap.md returns 0 matches; phantom extraction
