All 4 Augment Code review comments addressed in commit `ad9b8d1f`.

| Comment | File | Fix |
|---|---|---|
| [r3312667799](https://github.com/IronbellyOrg/IronClaude/pull/100#discussion_r3312667799) | `SPEC.md:55,264` | Pipeline diagram + flag example switched to `--generate spec` to match the §10 ship decision; `merged-requirements.md` filename preserved (it's part of v2's external contract). |
| [r3312667803](https://github.com/IronbellyOrg/IronClaude/pull/100#discussion_r3312667803) | `evals/evals.json` + `compare_live_runs.py` | Added `remediation_acceptance_scope: [4..11]` and `remediation_deferred_cases: [12]` to evals.json; rewrote `_validate_evals_sync` to use a `None` sentinel so missing keys emit an explicit `WARNING` instead of silently passing. |
| [r3312667807](https://github.com/IronbellyOrg/IronClaude/pull/100#discussion_r3312667807) | `grader.py` (parser) | Replaced flat-scalar `parse_yaml_simple` with `yaml.safe_load` (`pyyaml>=6.0` already in `pyproject.toml`); added frontmatter-detection so `.md` files with YAML frontmatter parse cleanly; added `_resolve_field` dotted-path helper; rewired the three `yaml_*` branches of `check_assertion` to use it with `str()` coercion and a non-numeric guard in `yaml_field_min`. |
| [r3312667808](https://github.com/IronbellyOrg/IronClaude/pull/100#discussion_r3312667808) | `grader.py` (write step) | Inserted `mkdir(parents=True, exist_ok=True)` before each variant `grading.json` write so partially-populated iteration folders no longer raise `FileNotFoundError`. |

**Verification:**
- All 12 iteration-2 evals at 100% pass rate after the changes (V2: 29/29, 27/27, 9/9, 25/25, 27/27, 12/12, 26/26, 28/28, 9/9, 25/25, 11/11, 23/23).
- `grading.json` output is byte-equivalent to the pre-fix baseline (0 substantive diffs).
- Per-fix acceptance checks: Fix 1 (`git grep` shows only §10/§16 hits), Fix 2 (`_validate_evals_sync` REPL test — 2 WARNINGs on missing keys, silent on matching config), Fix 3 (grader byte-equivalence on iteration-2 fixtures), Fix 4 (scratch dir with no variant subdirs survives and produces 0/N `grading.json` for each variant).

Generated with [Claude Code](https://claude.com/claude-code).
