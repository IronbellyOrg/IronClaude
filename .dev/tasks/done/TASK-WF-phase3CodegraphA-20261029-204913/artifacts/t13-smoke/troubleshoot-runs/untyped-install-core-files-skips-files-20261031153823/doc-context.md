# Documentation Context Card

**Generated**: 2026-10-31T15:38:23Z
**Wave**: 1.5
**Scope**: install_core_files

## Release context
- **Release**: None found
- **Artifacts**: None found
- **Summary**: Degraded release discovery returned no direct contract.
- **Confidence**: 0.0

## Architectural docs consulted
- `docs/getting-started/installation.md`: current. Plain installation preserves existing files; replacement requires an explicit overwrite operation.
- `docs/developer-guide/testing-debugging.md`: current. Core presence checks and overwrite guidance.
Parent captured both doc mtimes 1793453800; newest CLI source 1793455505. Difference 1705 seconds, below the 90-day threshold; discovery found no stale header markers. Discovery degraded because Auggie is unavailable.

## Restrictions / decisions that constrain the fix
- `docs/getting-started/installation.md:363`: "A plain `superclaude install` never replaces files you already have".
- `tests/cli/test_how_we_work_install.py:54`: "User rule: installers never delete, move or edit a file already in the target." The enclosing test uses force=False.
- `tests/cli/test_how_we_work_install.py:80`: unshipped files must remain unchanged even during forced installation.

## Re-frame signals
- Skipping existing destinations without force is documented preservation, not by itself a defect.
- No failing-run output, file list, destination, or force value was supplied. Whether the reported case satisfies that policy remains unobserved.
- Removing the preservation guard would violate the documented contract.
