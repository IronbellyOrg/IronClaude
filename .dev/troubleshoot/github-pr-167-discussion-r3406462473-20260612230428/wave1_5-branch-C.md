[
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 54,
    "quoted_text": "# label, optional bold before the colon, the REQUIRED colon, then more",
    "applies_to": "verdict parsing: markdown verdict line must include a colon after the Verdict label"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 56,
    "quoted_text": "#   * COLON required           -> rejects \"Verdict PASS\"",
    "applies_to": "verdict parsing: missing-colon markdown verdicts are intentionally rejected"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 105,
    "quoted_text": "required = [\"GOAL\", \"PRODUCT_SLUG\", \"PRD_SCOPE\", \"SCENARIO\"]",
    "applies_to": "parse-request semantic gate: these parsed request fields are required"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 118,
    "quoted_text": "return f\"Missing required fields: {', '.join(missing)}\"",
    "applies_to": "parse-request semantic gate: missing required fields produce a gate failure message"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 122,
    "quoted_text": "_RESEARCH_REQUIRED_SECTIONS = [",
    "applies_to": "research-notes semantic gate: defines the required section set"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 134,
    "quoted_text": "\"\"\"Check that research notes contain all 7 required sections.\"\"\"",
    "applies_to": "research-notes semantic gate: all seven sections are required"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 374,
    "quoted_text": "\"Parsed request missing required fields\",",
    "applies_to": "parse-request gate criteria: semantic-check failure message for required fields"
  },
  {
    "source_file": "src/superclaude/cli/prd/gates.py",
    "file_line": 393,
    "quoted_text": "\"Research notes missing required sections\",",
    "applies_to": "research-notes gate criteria: semantic-check failure message for required sections"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 51,
    "quoted_text": "\"\"\"Validate all 7 required research sections.\"\"\"",
    "applies_to": "research-notes semantic gate test: all seven sections are required"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 156,
    "quoted_text": "\"\"\"A 'Verdict rationale' heading with no PASS/FAIL value must not match.\"\"\"",
    "applies_to": "verdict parsing test: a Verdict heading without PASS/FAIL must not satisfy the gate"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 214,
    "quoted_text": "# sequential final completion phase 7. The completion phase must NOT",
    "applies_to": "parallel-instructions semantic gate test: final completion phase must not fail the gate"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 255,
    "quoted_text": "# The final phase is exempt ONLY when its heading marks it a completion",
    "applies_to": "parallel-instructions semantic gate test: final-phase exemption is restricted to completion-titled phases"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 274,
    "quoted_text": "# must be word-boundary anchored. A final WORK phase whose heading",
    "applies_to": "parallel-instructions semantic gate test: completion-signal matching must be word-boundary anchored"
  },
  {
    "source_file": "tests/cli/prd/test_gates.py",
    "file_line": 276,
    "quoted_text": "# \"complete\") must NOT be exempted -- it is real work and missing",
    "applies_to": "parallel-instructions semantic gate test: substring matches like Incomplete must not trigger completion exemption"
  }
]
