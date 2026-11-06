# Refactoring Plan

## Overview

- Base variant: V1 (sonnet:analyzer), `variant-1-original.md`
- Incorporated from: V3 (opus:refactorer) fallout check and wording anchor; V2 (haiku:qa) coverage confirmation; Round 2 and Round 2.5 corrections
- Changes planned: 6
- Overall risk: Low (the merged artifact is a review verdict; it changes no plan or repo file)
- Output artifact: `../merged-verdict.yaml` (reflect's merged verdict; the reviewer-card YAML shape, extended with `merge_method`, `base_variant` and `unaddressed_invariants`)

## Planned Changes

### Change #1: Correct V1 F1 (wording accuracy)
- Source: V1 F1 (base), corrected by V3 F1, installation.md:593, install_skill.py:47-48
- Target: base finding F1 (becomes merged M1)
- Integration approach: replace
- Rationale: debate points C-001, X-002. V1's "files the installer does not manage are never touched" and V3's "leaves user-created files alone" both fail (skill folders are deleted and re-copied, no backup). The seed-file and codegraph exceptions stay.
- Risk: Low

### Change #2: Replace V1 F3 (criterion 2) with the probe-corrected finding
- Source: V1 F3 (base); V3 Round 2 replacement text; INV-001, INV-003, INV-012
- Target: base finding F3 (becomes merged M2)
- Integration approach: restructure
- Rationale: debate points C-002, X-001, A-001. V1's staged-files argument was conceded wrong. The valid core is that plain `git diff --stat` cannot see staged or untracked changes and can list `.dev/tasks` files after `/sc:implement` stages and edits them. V3's baseline-based replacement fails on a correct run (INV-003), so the merged text excludes `.dev/tasks` and `.dev/reflect` and needs no saved baseline.
- Risk: Medium (the recommended text is orchestrator-derived from INV-003's fix and was not debated)

### Change #3: Add the CLAUDE.md naming gap
- Source: INV-010 (fault-finder), installation.md:593, install_core.py:57,69-73
- Target: new merged finding M3
- Integration approach: append
- Rationale: the README sentence would be weaker than the install guide on the file users most often edit.
- Risk: Low

### Change #4: Add V3's fallout and placement findings
- Source: V3 F2, F3, F4
- Target: new merged finding M4 (class none)
- Integration approach: append
- Rationale: unique contribution U-001 (High value); unchallenged in either round.
- Risk: Low

### Change #5: Add V2's coverage confirmation
- Source: V2 F1
- Target: new merged finding M5 (class none)
- Integration approach: append
- Rationale: unique contribution U-003; V2 kept this part in Round 2.
- Risk: Low

### Change #6: Record the unaddressed invariants
- Source: invariant-probe.md (INV-003, INV-012 HIGH; INV-001, INV-010 MEDIUM)
- Target: merged-verdict `unaddressed_invariants`
- Integration approach: append
- Rationale: HIGH + UNADDRESSED items block convergence and must stay visible to the consumer even though the plan text above addresses them.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why base prevails |
|------------|-------------------|-------------------|
| C-001 | V3 sources the wording fix from docs only | V1's code evidence is stronger (install_hooks.py:89-95, main.py:52); the fix text is the same |
| S-001 | V2's two-finding shape | All three label non-findings `minor`; V2's card carries no risk or edge-case content (0/5 on the floor dimension) |
| INV-008 | Mention `--target` in the README sentence | Out of scope for one sentence about the default path; logged as LOW |
| INV-007 | Exclude the seed file by name | Logged as LOW; "framework files it ships" is close enough for one sentence |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #2 | Medium | Consumer adopts untested criterion text | Keep the original criterion 2; the merged verdict is advisory and never edits the plan |
| others | Low | wording of a review verdict | n/a |

## Review Status

Auto-approved (non-interactive).
