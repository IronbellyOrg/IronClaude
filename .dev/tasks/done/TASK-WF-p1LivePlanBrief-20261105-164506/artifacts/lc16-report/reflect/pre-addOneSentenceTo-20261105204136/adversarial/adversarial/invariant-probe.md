# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis

Independent fault-finder (opus), six categories. Evidence column is the fault-finder's own citation; each was returned as read, not re-read by the orchestrator at this step.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The "before the edit" baseline in V3's criterion 2 will still exist when the reviewer checks it | UNADDRESSED | MEDIUM | r2-v3.md says to record the baseline but not where; /sc:implement reviewer is separate and a resume rebuilds state only from disk (sc-implement-protocol SKILL.md:105, :126-129); task evidence belongs in `<pkg>/artifacts/` (refs/managed-workspace.md:33) |
| INV-002 | state_variables | The plan can still be edited before execution starts | ADDRESSED | LOW | Package holds only the plan and source.md, no progress.md yet; plan edits allowed until the first start line (refs/managed-workspace.md:43) |
| INV-003 | guard_conditions | On a correct run `git status --porcelain` differs from baseline only by ` M README.md` and `git diff --cached --name-only` is unchanged | UNADDRESSED | HIGH | /sc:implement must stage `.dev/tasks/` incl. package, progress.md, artifacts (refs/managed-workspace.md:36; project CLAUDE.md "`.dev/tasks/` Is Always Staged"); staging changes both outputs, so the criterion fails on a correct run. Fix: exclude `.dev/tasks` and `.dev/reflect` from both comparisons |
| INV-004 | guard_conditions | `uv run pytest tests/docs` adds no status entries | ADDRESSED | LOW | .gitignore:2 `__pycache__/`, .gitignore:48 `.pytest_cache/` |
| INV-005 | count_divergence | "one sentence", "one hunk", "no [-...-] deletions" hold when the sentence is appended to README.md:64 | ADDRESSED | LOW | README.md:64 is one line; word-diff of an append yields only `{+...+}` |
| INV-006 | count_divergence | "deletes and re-copies each shipped skill folder" covers exactly the folders `--force` deletes | ADDRESSED | LOW | install_skill.py:47-48 via install_skills.py:102-110; stale `sc-*` deletion is independent of `--force` (install_skills.py:91-98) |
| INV-007 | collection_boundaries | "the framework files it ships" excludes the seed file that `--force` never overwrites | UNADDRESSED | LOW | install_hooks.py:89-95 calls the seed shipped yet never overwritten even with `--force`; read literally the phrase includes it |
| INV-008 | collection_boundaries | Everything `--force` overwrites lives in `~/.claude` | UNADDRESSED | LOW | `--target` defaults to `~/.claude/commands/sc` (main.py:32); a custom target writes elsewhere |
| INV-009 | collection_boundaries | "without keeping a backup" is true for every file `--force` changes | ADDRESSED | LOW | settings.json is rewritten but backed up first (install_hooks.py:302-308, :404-409); wording limited to shipped files stays accurate |
| INV-010 | interaction_effects | "framework files" tells readers their own `~/.claude/CLAUDE.md` will be replaced | UNADDRESSED | MEDIUM | install_core.py:57,69-73 overwrite `core/*.md` incl. CLAUDE.md and RULES.md; installation.md:593 names both, the consensus sentence does not |
| INV-011 | interaction_effects | New sentence does not contradict nearby `--force` text | ADDRESSED | LOW | README.md:75 uses the same term; README.md:68 already says to back up edits |
| INV-012 | sufficiency_challenge | The consensus changes alone make the plan correct and executable | UNADDRESSED | HIGH | Disproved by INV-003 (criterion 2 fails on a correct run); plan title and goal (plan:12, plan:15) still say "overwrites existing files in ~/.claude" and would contradict the corrected criterion |
| INV-013 | sufficiency_challenge | Consensus wording still meets the spec and README formatting rules | ADDRESSED | LOW | One sentence containing the statement in narrower form; MD013 disabled (.markdownlint.json:4); tests/docs/test_retired_docs_absent.py:37-49 checks links only |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 7
- **UNADDRESSED**: 6
  - HIGH: 2 (INV-003, INV-012)
  - MEDIUM: 2 (INV-001, INV-010)
  - LOW: 2 (INV-007, INV-008)

Fault-finder limit: it did not run criterion 2 against a real /sc:implement run; the staging conflict comes from reading the protocol rules.
