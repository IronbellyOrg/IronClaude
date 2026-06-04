# Installer Mapping Pytest Summary (Step 4.2)

**Test selection used:** `tests/unit/test_cli_install.py` (the F2 regression guard lives in the `TestProtocolSkillInstallMapping` class within this module — the nearest installer test module).
**Command:** `uv run pytest tests/unit/test_cli_install.py -v`
**Raw output:** `installer-pytest-output.txt`
**Date:** 2026-06-03

- **Overall result:** PASS (exit 0)
- **Total tests run:** 17
- **Passed:** 17
- **Failed:** 0
- **Errored:** 0
- **Skipped:** 0
- **Failed test names:** none
- **Pytest summary line:** `17 passed in 0.19s`

F2 guard (`TestProtocolSkillInstallMapping`, 5 tests) all passed:
- `test_new_init_lite_protocol_is_not_command_backed`
- `test_sample_existing_protocol_skills_not_command_backed`
- `test_bare_sc_command_mapping_still_works`
- `test_no_available_protocol_skill_is_command_backed`
- `test_install_all_skills_keeps_protocol_skills_standalone`
