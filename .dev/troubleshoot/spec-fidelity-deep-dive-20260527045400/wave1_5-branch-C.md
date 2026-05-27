```json
[
  {
    "source_file": "src/superclaude/cli/roadmap/structural_checkers.py",
    "file_line": "155-176",
    "quoted_text": "FIX_GUIDANCE_TEMPLATES = { 'threshold_contradicted': '...', 'security_missing': '...', 'dep_direction_violated': '...', 'coverage_mismatch': '...', 'dep_rule_missing': '...' }",
    "applies_to": "Per-rule_id fix guidance for the agent. phantom_id is NOT in this dict — phantom_id findings get the generic 'Address {mismatch_type} in {dimension} dimension' guidance with no instruction on whether to remove, rename, or add IDs."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/structural_checkers.py",
    "file_line": "205-213",
    "quoted_text": "template = FIX_GUIDANCE_TEMPLATES.get(f.rule_id); if template and f.fix_guidance.startswith('Address '): try: f.fix_guidance = template.format(spec_quote=f.spec_quote or '', roadmap_quote=f.roadmap_quote or ''); except (KeyError, IndexError): pass",
    "applies_to": "_route_findings template-application loop. The 'no phantom_id template' gap surfaces here — only listed rule_ids get actionable guidance."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/structural_checkers.py",
    "file_line": "380",
    "quoted_text": "phantom_ids = roadmap_ids - spec_ids",
    "applies_to": "THE comparator. Raw Python set difference of strings. No canonicalization step before the operation."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/spec_parser.py",
    "file_line": "329",
    "quoted_text": "\"D\": re.compile(r\"\\bD-?\\d+\\b\")",
    "applies_to": "D-family ID extraction regex — LENIENT (matches both D1 and D01 and D-01) but emits the raw matched form. Inconsistency between lenient extraction and strict comparison is the root mechanical defect."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/spec_parser.py",
    "file_line": "340-344",
    "quoted_text": "for family, pattern in _REQUIREMENT_PATTERNS.items(): ids = sorted(set(pattern.findall(text))); if ids: result[family] = ids",
    "applies_to": "extract_requirement_ids — return format preserves the raw matched form for each family. No normalization applied here either."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/convergence.py",
    "file_line": "440",
    "quoted_text": "max_runs: int = 3",
    "applies_to": "Hard default of 3 runs. The executor passes 3 (verified via roadmap-state.json runs[] length). No CLI flag wired to raise this in convergence mode — --max-runs only affects --allow-regeneration BACKUP path per BACKUP-WORKAROUND.md."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/convergence.py",
    "file_line": "539",
    "quoted_text": "if active_highs == 0: ledger.credit(CONVERGENCE_PASS_CREDIT); ... return ConvergenceResult(passed=True, ...)",
    "applies_to": "Pass condition. Binary: 0 active HIGHs → pass; anything else → continue or halt. No MANUAL_TRIAGE classification, no per-rule_id allowlist of acceptable residual findings."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/convergence.py",
    "file_line": "653-668",
    "quoted_text": "halt_msg = f'Convergence not reached after {max_runs} runs. Remaining active HIGHs: {final_highs}. TurnLedger: available={ledger.available()}, consumed={ledger.consumed}'",
    "applies_to": "Halt formatter. Mentions only count + budget — no rule_id breakdown, no signal that findings are structurally-unfixable vs agent-failure, no actionable next step. Misleads the user about whether the loop ran out of budget (it didn't — available=31) or out of attempts."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/remediate_executor.py",
    "file_line": "309-362",
    "quoted_text": "if ratio > (_DIFF_SIZE_THRESHOLD_PCT / 100.0): if allow_regeneration: ...proceeding; else: ...rejecting. Use --allow-regeneration to override.",
    "applies_to": "30% diff guard. Per-patch granularity (good), but no per-rule_id tier — the only correct fix for a 54-ID schema migration would exceed 30% and be rejected by default."
  },
  {
    "source_file": "tests/roadmap/test_convergence.py",
    "file_line": "923-949",
    "quoted_text": "def decreasing_checkers ... if n == 1: findings = [F-001, F-002]; elif n == 2: findings = [F-001]; else: findings = [] ... assert result.passed; assert result.run_count == 3; assert result.final_high_count == 0",
    "applies_to": "Convergence loop test only validates the HAPPY PATH (monotonically decreasing findings → eventual zero). No test asserts behavior when findings flatline (the present TUIBBS failure shape: 58 → 54 → 54 → 54). The test suite has no coverage for 'structurally-unfixable findings' — fixing this gap is part of the remediation surface."
  },
  {
    "source_file": "src/superclaude/cli/roadmap/integration_contracts.py",
    "file_line": "445",
    "quoted_text": "def _canonicalize_identifiers(text: str) -> frozenset[str]:",
    "applies_to": "PRECEDENT for canonicalization in this codebase. Used by the anti-instinct gate (Fix B Merged 2026-05-25, KNOWLEDGE.md:156-205) to collapse semantically-identical mechanism IDs. Pattern is locally established; extending it to D-family ID comparison is consistent with existing precedent, not novel."
  }
]
```
