# Option C: required phase, advisory doctor, receipt plus documented removal

Read `context.md` in this folder first; this option adds only the contract.

## Contract
- **Required phase.** Same as Option A: a failed codegraph phase makes `superclaude install` exit 1 after every other phase ran, with the failed stage named on stderr. This is what makes "installed by default" true and lets Coder CI prove it through the existing exit-0 expectation.
- **Doctor: report, fail only on a broken registration.** New `_check_codegraph` fails only when the user entry `codegraph` exists and its `command` is not an executable file (a registration that would break every Claude session). Missing binary, version drift and upstream leftovers (`CODEGRAPH_START` block, `codegraph prompt-hook`) are reported in `details` with `passed: True`, because the install phase already enforces presence and doctor runs right after it in `./update.sh`.
- **Removal: receipt plus documented commands, no new CLI flag.** After a verified download IronClaude writes `~/.codegraph/.superclaude-receipt.json` (tag, tarball sha256, link targets). Docs give the removal: `claude mcp remove codegraph --scope user`, then delete the receipt's listed paths. `superclaude install --list` prints, from the receipt, exactly which paths IronClaude owns ("owned: ~/.codegraph/versions/v1.6.2 …" or "external: /usr/local/bin/codegraph, not owned"). Baked or external binaries and `.codegraph/` project indexes are never listed as removable.
- **Old version dirs.** On a pin bump the phase installs the new dir, flips links, and deletes only receipt-listed older version dirs that no running daemon uses (check `~/.codegraph/daemons/`), otherwise leaves them for the next run.

## Code size estimate
`install_codegraph.py` about 170 lines; `install_mcp.py` +60; `doctor.py` +30; `main.py` +30. Tests about 28 cases.

## Strengths
- Keeps the hard guarantee where it matters (install exit code, which both `./update.sh` and Coder already gate on) without doubling it in doctor.
- Ownership is recorded, so removal instructions are exact and safe, without a CLI uninstall surface.
- Doctor catches the one state that harms every session (a dangling registered command) yet does not fail on drift that the next install fixes.

## Weaknesses
- Coder must bake first (same as A) or the slug fails offline.
- The receipt is a small extra file to read and test.
- Users who want one-command removal must copy two commands.
