# Merge Log

## Metadata

- Base: Variant 1 (sonnet:analyzer), `variant-1-original.md`
- Executor: merge-executor
- Changes planned: 6 (refactor-plan.md, Changes #1-#6)
- Changes applied: 6
- Status: complete; merged artifact written and YAML parses
- Output: `../merged-verdict.yaml`
- Timestamp (UTC): 2026-11-05T20:56:23Z

## Changes Applied

### Change #1: Correct V1 F1 (wording accuracy) -> M1
- Status: applied (replace)
- Taken: V1 F1's seed-file and codegraph exceptions (install_hooks.py:89-95, main.py:52) and V1 F2's force-flow evidence (install_core.py:69); the skill-folder delete-and-re-copy and no-backup correction from V3 F1 as corrected in Round 2 by all three advocates (install_skill.py:47-48, installation.md:593); settings.json backup citation (install_hooks.py:404-409) from invariant-probe INV-009.
- Dropped: V1's "files the installer does not manage are never touched", V3's "leaves user-created files alone", and V1's wrong install_hooks.py:250 citation (conceded in Round 1 and Round 2).
- Provenance: `source` field on M1 = V1 F1 (base) + V3 F1 + Round 2 (C-001, X-002).

### Change #2: Replace V1 F3 (criterion 2) -> M2
- Status: applied (restructure)
- Taken: V1 F3's target (plan line 30) and its `git diff --word-diff` idea; the valid core from C-002 (plain `git diff --stat` misses staged and untracked changes); INV-003's fix (exclude `.dev/tasks` and `.dev/reflect`); INV-001's baseline-storage gap. The replacement criterion text is the exact text given by the orchestrator and is marked as orchestrator-derived from INV-003 and not debated. V3's Round 2 baseline-based text is named and rejected because it fails on a correct /sc:implement run.
- Tag set to `inferred`: the staging conflict comes from reading protocol rules (invariant-probe.md line 32), not from a real run.
- Provenance: `source` field on M2 = V1 F3 (base) + V3 Round 2 (rejected) + INV-001, INV-003, INV-012.

### Change #3: Add the CLAUDE.md naming gap -> M3
- Status: applied (append)
- Taken: INV-010 (install_core.py:57, :69-73; installation.md:593). Recommendation inserts "(including `CLAUDE.md` and `RULES.md`)" into the Task 1 sentence.
- Provenance: `source` field on M3 = invariant-probe INV-010.

### Change #4: Add V3's fallout and placement findings -> M4
- Status: applied (append, class none)
- Taken: V3 F2 (placement, README.md:64, :66-75), F3 (no contradiction with README.md:75), F4 (installation.md:283, :591, upgrading.md:56-60; test_retired_docs_absent.py); V1 F4 anchor check (README.md:55); A-002 resolution (no test catches a wrong sentence; test range 37-49 from the debate scoring matrix).
- Provenance: `source` field on M4 = V3 F2-F4 (U-001) + V1 F4 + A-002.

### Change #5: Add V2's coverage confirmation -> M5
- Status: applied (append, class none)
- Taken: V2 F1 (source.md:1; plan lines 19-30 from V2 F2's span and the debate). V2 F2's "falsifiable" claim not carried (conceded, X-001).
- Provenance: `source` field on M5 = V2 F1 (U-003).

### Change #6: Record the unaddressed invariants
- Status: applied (append)
- Taken: INV-003 and INV-012 (HIGH) copied from invariant-probe.md with id, category, assumption, severity into `unaddressed_invariants`; INV-001 and INV-010 (MEDIUM) listed in `unaddressed_invariants_warnings`. `plan_alignment_note` records INV-012's plan title and Goal fix (plan lines 12 and 15) plus criterion 1.
- Provenance: invariant-probe.md (Round 2.5).

## Post-Merge Validation

- Structural integrity: `yaml.safe_load` parses `merged-verdict.yaml` (run with `uv run python -I`). Top-level keys are in the required order; findings are exactly M1-M5, each with id, claim, citation, tag, class, severity, recommendation, source. All five severities are `minor`; M1-M3 class `gap`, M4-M5 class `none`. The M2 recommendation contains the required replacement text byte-for-byte (checked by substring match).
- References: every cited file exists on disk (checked by script). Lines re-read by the executor this session: plan lines 12-30 (TASK-WF-addOneSentenceTo-20261105-204034.md), README.md:53-75, installation.md:588-595, install_skill.py:42-53, install_core.py:50-77, install_hooks.py:84-96, main.py:30-54, refs/managed-workspace.md:30-44; all matched the claims they support. Taken from the inputs and not re-read: install_hooks.py:404-409 (invariant-probe INV-009), installation.md:283, upgrading.md:56-60 (V3 F4, debate), tests/docs/test_retired_docs_absent.py:37-49 (debate scoring matrix, INV-013), source.md:1 (V2 F1). None could be confirmed false; none were found missing.
- Contradictions: none new versus the inputs. Two known differences are deliberate and come from the plan: M2 rejects V3's Round 2 criterion text that base-selection.md lists as a strength to incorporate (refactor-plan.md Change #2 overrides it via INV-003), and M2 is tagged `inferred` while M1 uses V1's `grounded` tag.

## Summary

- Planned: 6
- Applied: 6
- Failed: 0
- Skipped: 0
