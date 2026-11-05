# Hypothesis: the Tier 1 trust gate is right in place and fields, but its evaluation command and file identity leave bypasses

**Agent**: security-engineer (lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing trust gate, plus a gate evaluated inside the untrusted project context
**Claim class**: `mixed`
**Evidence class**: `runtime_repro` (parent probe probe-lock-trust.out:6; parent falsification run in audit.log)
**Verdict direction**: `AFFIRM` (C3); agrees with the Tier 1 cause, extends fix item 3, disagrees with its command form
**Consistency with docs**: conflicts (the design has no trust model, doc-context.md)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:87 @ attended Claude Code session, operator checkout, merge in progress, operator credentials
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
The owner's three triggers belong before `uv lock`. Within scope the gate has three gaps: (1) `uv run --no-sync python -I` is the wrong runtime: it discovers the PR's project from the cwd, reads its pyproject.toml, uv.toml and .python-version, creates `.venv` in the work tree (audit.log), and in a non-dev target project has no `superclaude`, so every Tier 1 would halt; `-I` still processes site-packages .pth files, so in a dev checkout the editable gate is imported from the PR's tree. (2) The checked file must be `<toplevel>/pyproject.toml`, the one `uv lock` reads, with uv run from the top level; step 5 does not say so. (3) A `[tool.uv.sources]` value is a table or a list of tables with markers; every entry must be checked and other shapes halt. A non-empty `project.dynamic` is a needed trigger (asserted: a dynamic project runs the backend from build-system.requires on in-tree code); static + backend-path is unobserved but the gate fires on backend-path alone.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | probe-lock-trust.out:6; behaviour-definition: row 1 | "in-tree backend executed: yes" |
| E2 | command_output | audit.log (parent falsification run) | `uv run --no-sync --offline python -I` created .venv; backend executed: no |
| E3 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:84-90 | uv with no stated directory, no pyproject check |
| E4 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:228-230 | classifier runtime: `uv run python` in a dev checkout "or the installed package's interpreter" |
| E5 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:31 | conflicts.py functions are called in prose with data passed in |
| E6 | source_citation | src/superclaude/pr_submit/conflicts.py:16, :19-21 | no I/O; fail closed |
| E7 | test_assertion | tests/pr_submit/test_conflict_sync_protocol.py:40 | fenced commands must start with git/gh/uv/make/jq or scripts/ |
| E8 | source_citation | doc-context.md (INV-033) | uv.lock gitignored in this repo; Tier 1 never fires in the dev checkout |
| E9 | unobserved | behaviour-definition: row 2 | path/editable source builds the local package |

## Proposed Fix
Keep Tier 1 items 1, 2, 4, 5. Replace item 3: in step 5, after the precheck, read `pyproject.toml` at the work-tree top level as text and call `lock_trust_findings(text)` in prose, in the same classifier runtime used for `conflict_plan` (SKILL.md:228-230), never through `uv run` in the work tree; any finding: abort, `sync_tier3`, naming the field; state that `uv lock` and `uv lock --check` run from the top level. Sources checked per entry (table or list of tables; other shapes unreadable). (Card also proposed: a missing or non-table `[project]` returns unreadable, with a test.)

## Confidence
Self-reported 0.80 (calibrator re-grades).

## Risks
- The dev-checkout case still imports the PR's gate code; moot for Tier 1 here (E8); covered by the trust note.
- A missing-[project] rule would halt a virtual workspace root.
- Out-of-scope residuals for the report: a PR-added root uv.toml (find-links, override-dependencies); `name @ file://` direct references in dependencies, dependency-groups or uv override/constraint lists; sdists from find-links or an index; workspace sources and member pyprojects; git and URL sources; a .python-version naming an interpreter path; a tracked core.hooksPath running hooks between the gate and `uv lock`; VAL and the step 9 commit hooks run PR code.

## If I'm wrong, it's probably because...
The installed-runtime call is not available at step 5, or uv reads pyproject from elsewhere for a root uv.lock.

## Falsification standard
Claim (1) is false if `uv run --no-sync python -I -c "import superclaude.pr_submit.conflicts"` succeeds in a non-dev uv project where superclaude exists only in pipx. The trigger list is false if a gate-passing pyproject makes `uv lock --offline` write the marker. Pending probes (not run): static + backend-path; path source as table and list; uv.toml with [sources]; .python-version naming an in-tree script.

## Alternatives considered
- `uv run --no-sync python -I`: rejected for (1).
- Halt whenever a root uv.toml exists: outside the owner's fields; owner decision needed.
- `git show :0:pyproject.toml`: same bytes after the precheck, not the file uv reads.
- `uv lock --no-build`: hides the reason.
