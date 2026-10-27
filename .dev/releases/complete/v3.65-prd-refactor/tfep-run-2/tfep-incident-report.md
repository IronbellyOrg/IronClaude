# TFEP Incident Report

- **Trigger**: Second failed retest after TFEP run 1 (2 remaining failures)
- **Escalation count**: 2
- **Failing tests**:
  - test_inline_code_scaffold_term_is_medium
  - test_code_block_still_medium
- **Root cause**: Mixed cause: (1) implementation regression from over-broad discharge-intent skipping; (2) test fixture mismatch with strict FR-MOD1.1 vocabulary contract.
- **Solution**: Remove/narrow unconditional discharge-intent `continue`; keep strict vocabulary; update code-block test fixture token to in-vocabulary scaffold term.
- **Outcome**: escalated (forensic success, remediation block ready)
- **Forensic artifacts**: `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/tfep-run-2/`
