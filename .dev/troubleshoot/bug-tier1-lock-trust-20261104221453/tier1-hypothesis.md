# Hypothesis: Tier 1 runs `uv lock` on a merged pyproject.toml that the PR controls, so the PR's build backend runs with the maintainer's credentials

**Agent**: root-cause-analyst (security lens; worker troubleshoot-analyst)
**Tier**: 1
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing trust gate (unvalidated input to a command that executes code)
**Claim class**: `mixed`
**Evidence class**: `runtime_observed` (parent probe, tier1-observation.md ## Probe)
**Verdict direction**: `AFFIRM` (confirms C3)
**Consistency with docs**: conflicts (the design has no trust model and treats the tracked pyproject.toml as safe; doc-context.md, OQ-31)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:87 @ attended Claude Code session, operator checkout with the merge in progress, operator credentials

producer-citation-check: skipped — menu absent or empty (producers.md: observation-kind trace, header-only table)

## Claim
Step 5 runs `uv lock` and `uv lock --check` on the merged work tree; nothing reads the merged pyproject.toml first. When it declares `build-system.backend-path`, a non-empty `project.dynamic`, or a path or editable `[tool.uv.sources]` entry, uv imports and runs code from the tree to get metadata. In a Tier 1 plan pyproject.toml merged without conflict, so the PR's version is used. Tier 1 is the default, so this happens without the operator opting in.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | tier1-observation.md `## Probe` (probe-lock-trust.out:5) | "in-tree backend executed: yes" with backend-path=["."] and a dynamic version, although `uv lock` exited 1 |
| E2 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:84-90 | precheck, `git checkout --ours -- uv.lock`, `uv lock`, `uv lock --check`; no pyproject check |
| E3 | source_citation | src/superclaude/pr_submit/conflicts.py:202-210 | the only mechanical rule is uv.lock with sources ("pyproject.toml",) |
| E4 | source_citation | src/superclaude/pr_submit/conflicts.py:11-21 | stdlib allowlist base64, re, dataclasses, typing; no I/O; fail closed |
| E5 | test_assertion | tests/pr_submit/test_conflicts_core.py:2445, :2473 | `_ALLOWED_STDLIB`; `__import__` banned |
| E6 | source_citation | pyproject.toml:16; .github/workflows/test.yml:22 | requires-python >=3.10; CI runs 3.10, which has no tomllib |
| E7 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:296 | `sync_tier3` row covers only the Tier 2 escalation |
| E8 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:219; src/superclaude/commands/pr-submit.md:54 | default Tier 1; no trust note |
| E9 | unobserved | behaviour-definitions.md row 2 | uv building path/editable sources asserted, not probed |

## Proposed Fix
1. conflicts.py: guarded `try: import tomllib` / `except ImportError: tomllib = None` (Python 3.10); `LOCK_TRUST_UNREADABLE = "pyproject.toml unreadable"`; pure `lock_trust_findings(pyproject_text: str) -> list[str]`: `[LOCK_TRUST_UNREADABLE]` when tomllib is None, on a parse error, or on a bad shape (non-table build-system/project/tool/uv/sources, a source neither a table nor a list of tables); else, in order, "build-system.backend-path" (key present), "project.dynamic" (truthy), and for each sorted source name "tool.uv.sources.<name> (path)" when any entry has `path`, "tool.uv.sources.<name> (editable)" when any entry has `editable = true` (a source value is a table or a list of tables with markers).
2. Allowlist: add tomllib to `_ALLOWED_STDLIB` (test_conflicts_core.py:2445) and the docstring (conflicts.py:11).
3. conflict-mechanical.md step 5: after the precheck and before `git checkout --ours`, evaluate `lock_trust_findings` on the work-tree pyproject.toml (the file `uv lock` reads; equal to stage 0 once the precheck passed); any finding: abort (section 9), `sync_tier3`, naming the fields; `uv lock` never runs. If a command form is given, it is `uv run --no-sync python -I ...` (plain `uv run` syncs and builds the project). Extend the :296 row.
4. Trust note in refs section 6, SKILL.md (Will Not Do, near :219) and commands/pr-submit.md:54: "Conflict resolution and VAL run the project's build and test code on the merged tree; run pr-submit only on PRs from collaborators you trust with your credentials."
5. Tests (test_conflicts_core.py): one per trigger (backend-path, dynamic, path source as a table, editable source in a list of tables), skipped below 3.11; clean pyproject returns []; parse error returns [LOCK_TRUST_UNREADABLE]; tomllib monkeypatched to None returns [LOCK_TRUST_UNREADABLE] on every Python; a protocol pin for the gate in test_conflict_sync_protocol.py.

## Confidence
Self-reported 0.85 (calibrator re-grades).

## Risks
- On Python 3.10 every Tier 1 halts (fail closed): Tier 1 is effectively off there.
- In this repo's own dev checkout `superclaude` is imported from the PR's tree, so a PR could edit the gate; only the trust note covers it.
- Git, URL, sdist and workspace-member builds `uv lock` can trigger are outside the owner's trigger list.
- The Wave 0 preflight `uv run python -c` (SKILL.md:229) already syncs the PR head in a dev checkout.

## If I'm wrong, it's probably because...
`uv run --no-sync` still builds the project, or uv runs the backend for fields outside the list.

## Falsification standard
In the probe's scratch project `uv run --no-sync python -I -c ...` must leave no marker file (parent ran it 2026-11-04T22:22Z: "backend executed: no", audit.log). A pyproject for which `lock_trust_findings` returns [] but `uv lock` writes the marker would falsify the trigger list.

## Alternatives considered
- Default `--conflict-max-tier 0` (option A): owner rejected.
- `uv lock --no-build`: fails on dynamic root metadata, hiding the reason.
- Check at plan time: owner specified before `uv lock`.
- `git show :0:pyproject.toml`: same bytes after the precheck, not the file uv reads.
