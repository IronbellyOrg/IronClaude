# Documentation Context Card
**Generated**: 2026-10-31T15:24:43Z
**Wave**: 1.5
**Scope**: install_core_files
## Release context
Branch A unavailable: selected analyst roster violates the loaded protocol's closed roster. Native release search found backlog references, not an established current/complete release constraint.
## Architectural docs consulted
Branch B unavailable. Parent fallback: docs/getting-started/installation.md:260-264 assigns overwrite to --force. Currency: current (parent stat: doc=1793453800, implementation=1793455505; difference below 90 days; no deprecated marker in inspected section).
## Restrictions / decisions that constrain the fix
Branch C unavailable. Parent fallback: tests/cli/test_how_we_work_install.py:53-75 requires existing files to remain unchanged without force. Test was read, not run.
## Re-frame signals
- Existing-target skips without force agree with the documented overwrite option and preservation test.
- This does not establish which files or options were involved in the user's run. No production change is justified by the supplied evidence.
