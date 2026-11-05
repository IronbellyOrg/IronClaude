# Merge Execution Log

## Metadata
- Base: Variant B (`variant-2-original.md`, reviewer 2, qa persona, haiku class)
- Incorporated: Variant A (`variant-1-original.md`, reviewer 1, analyzer persona, sonnet class); Round 2.5 probe (`invariant-probe.md`, fault-finder)
- Plan: `refactor-plan.md` (13 changes, auto-approved 2026-11-05T18:27:31Z)
- Merged artifact: `../merged-verdict.yaml` (YAML reviewer card; provenance as `# Source: ...` YAML comments)
- Executor: merge-executor agent
- Changes applied: 13 of 13 planned
- Status: success
- Timestamp: 2026-11-05

Citation check before merging: every code, test and doc line the plan carries into a finding was re-read in this step (`ccsession:75, 96-98, 109-114, 121-124, 819-836, 846-849, 1651-1652, 1671, 1799, 1801, 1859, 1861, 1866, 1868`; `ccsession-orca:14-17, 132-137, 204-212, 247, 249`; `hooks/session-name.sh:196-212`; `install_ccsession.py:104-113`; `test_ccsession_tag.py:1134-1153, 1177-1184, 1251, 1806-1811`; `test_ccsession_tiers.py:112, 362, 445, 500, 525`; `test_install_ccsession.py:51-67, 224-238`; `tests/cli/test_update_command.py:198-208`; `D08-ccsession.md:23`; `E01-ccsession-tier-policy.md:21`; `source.md:1`; PLAN:15-148; `sc-reflect-protocol/SKILL.md:985-1017, 1056`). All matched the plan's description. No citation was altered or invented; base citations were kept as they were and new ones were taken from the plan, Variant A or the probe.

## Changes Applied

### Change 1: Task 5 help sentinel (M-F1)
- **Status**: Applied
- **Source**: Variant A F1 (`recommended_change`, evidence); Round 2.5 probe (fault-finder) INV-008
- **Target**: Base F1 -> M-F1
- **Before**: B's remedy: retarget the awk marker or move the paragraph above it; guard tokens `set -e` and `CC_CLAUDE_FLAGS=`.
- **After**: B's claim kept verbatim, with one parenthetical the plan names ("also occurs at ccsession:75 and :98, above the sentinel"). Remedy replaced with the plan's four parts: usage entry next to `ccsession:96-97` above the sentinel; keep line 109's `# The wrapper always runs` prefix or change `ccsession:1652` in the same edit; rewrite PLAN:97 and PLAN:100; guard test with `set -e` and `CLAUDE_BIN=`. Evidence appended: `ccsession:96-98, 109-114, 110-113, 121, 123`, `test_ccsession_tag.py:1134-1144`. Class Regression, severity blocking unchanged.
- **Provenance tag**: `# Source: Base (original, modified) — Change 1 ... Variant A F1 ... Round 2.5 probe (fault-finder) INV-008`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 2: Task 1 red-log criterion (M-F2)
- **Status**: Applied
- **Source**: Base F2; debate U-004 (A R2 response 1, B R2 response 3, B calibrator note)
- **Target**: Base F2 -> M-F2
- **Before**: Two prongs given equal weight; class Drift.
- **After**: First prong (the `--verbose` + `default` test passes on old code) carries the claim; the empty-`CC_CLAUDE_FLAGS` point is stated as an ambiguity. Class Regression (SKILL.md:1009, :1017 cited in the provenance comment). Severity blocking, evidence and B's replacement criterion text unchanged.
- **Provenance tag**: `# Source: Base (original, modified) — Change 2 (U-004 ...)`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 3: Task 1 bypass test can start the real Claude (M-F3)
- **Status**: Applied
- **Source**: Round 2.5 probe (fault-finder) INV-007
- **Target**: New finding M-F3 after M-F2; `plan_ref: Task 1`, class Drift, severity blocking
- **Before**: Did not exist.
- **After**: Narrowed claim as the plan states (the finding stands on the exec of `claude` with the bypass flag; the stdin hang is called the less likely outcome). Evidence PLAN:36, PLAN:39, `test_ccsession_tag.py:1145-1153, 1177-1184`, `ccsession:123, 1868`. Remedy: `_label_launch` environment via `extra_env`, `stdin=subprocess.DEVNULL`, timeout, assert the fake Claude did not run.
- **Provenance tag**: `# Source: Round 2.5 probe (fault-finder), INV-007 — merged per Change 3`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 4: Global exit-2 scope (M-F4)
- **Status**: Applied
- **Source**: Base F3; Variant A F2 (U-001 orca trace); A R2 N1, N4; Round 2.5 probe (fault-finder) INV-011
- **Target**: Base F3 -> M-F4
- **Before**: Enumerated subcommand list as the scope; "breaks tab-title cleanup and name listing"; remedy test used `--list`.
- **After**: Scope "every invocation, including `--help`", subcommands named as examples only; impact split into visible (`--help`, `--list`, `--rm`) and silent (hook calls, installer `--migrate-names`), plus the orca messages and "no bypass leaks". "Breaks tab-title cleanup and name listing" dropped. Evidence appended: `ccsession-orca:132-137, 204-212, 247, 249`, `hooks/session-name.sh:196-212`, `install_ccsession.py:104-113`. Remedy: state scope and pin with a bad value + `ccsession --help` exits 2 test, or defer only the exit under M-F5. Class Drift, severity minor, `plan_ref: Constraints` kept. The INV-011 extra subcommand lines (`ccsession:668, 706, 1676-1690`) were not added, because the plan says to give subcommands as examples only and does not list those anchors.
- **Provenance tag**: `# Source: Base (original, modified) — Change 4 ... Variant A F2 ... Round 2.5 probe (fault-finder) INV-011`
- **Validation**: Structural integrity OK | References OK (M-F5 resolves) | Contradictions OK

### Change 5: Launch-scoping must keep the flag choice at line 124 (M-F5)
- **Status**: Applied
- **Source**: Round 2.5 probe (fault-finder) INV-017
- **Target**: New finding M-F5 after M-F4; `plan_ref: Constraints`, severity minor
- **Before**: Did not exist.
- **After**: Claim and evidence as in the plan (`ccsession:819-836, 846, 847-849, 1671`, PLAN:20, PLAN:23, `source.md:1`). The plan's class "Regression (latent)" is written as `class: Regression` with "Latent:" leading the claim and in the provenance comment, so the class field stays one of the four taxonomy values.
- **Provenance tag**: `# Source: Round 2.5 probe (fault-finder), INV-017 — merged per Change 5`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 6: Caller-passed flags still apply; Goal overstates the spec (M-F6)
- **Status**: Applied
- **Source**: Round 2.5 probe (fault-finder) INV-016, INV-003 folded in
- **Target**: New finding M-F6 after M-F5; `plan_ref: Constraints`, class Drift, severity minor
- **Before**: Did not exist.
- **After**: Claim per the plan (Orca's default option passes through `"$@"`; add-on profiles and the env file can reassign `CC_CLAUDE_FLAGS`; spec wording holds; issue-390 use case unaffected). Evidence PLAN:15, `ccsession-orca:14-17, 247, 249`, the six launch lines, `ccsession:819-836`, `test_ccsession_tag.py:1806-1811`, `source.md:1`. Remedy: reword PLAN:15; add the caller-flags sentence to Tasks 5, 6 and 9.
- **Provenance tag**: `# Source: Round 2.5 probe (fault-finder), INV-016 with INV-003 folded in — merged per Change 6`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 7: Env-file clause (M-F7)
- **Status**: Applied
- **Source**: Base F4; A-008; C-005
- **Target**: Base F4 -> M-F7
- **Before**: "sourcing at ccsession:846-849"; class Drift; remedy test or drop clause.
- **After**: "assigned at ccsession:846 and sourced at ccsession:847-849"; PLAN:121 imprecision added (A-008); class Regression (orchestrator consistency correction, noted as not a debate ruling); remedy extended with the `test_ccsession_tag.py:1182` note and the PLAN:121 rewording. Severity minor kept. Base evidence `ccsession:846` and `ccsession:849` kept unchanged; `ccsession:124`, `ccsession:847-849` and `test_ccsession_tag.py:1182` appended.
- **Provenance tag**: `# Source: Base (original, modified) — Change 7 (U-005, C-005, A-008)`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 8: Task 3 `CC_CLAUDE_FLAGS` leak, extended to unisolated tests (M-F8)
- **Status**: Applied
- **Source**: Base F6; Variant A F3; A-007
- **Target**: Base F6 -> M-F8
- **Before**: Remedy only the tiers fixture / `_launch_env`.
- **After**: B's claim kept verbatim. Remedy adds A's alternatives (`CC_CLAUDE_FLAGS=""` or `monkeypatch.delenv`) and one sentence on clearing `CCSESSION_PERMISSIONS` in `test_install_ccsession.py:51-67, :224-238` and `tests/cli/test_update_command.py:198-208`, or launch-scoping under M-F5. A's aside about the excluded-names tuple not carried. Evidence appended: `test_ccsession_tiers.py:101-122, 362-384`, the three test sites. In this step, `:224-238` and `test_update_command.py:198-208` were confirmed to pass `**os.environ` to a `--help` run; `:51-67` calls `wire_ccsession`, which runs `--migrate-names` with `**os.environ` (`install_ccsession.py:104-113`).
- **Provenance tag**: `# Source: Base (original, modified) — Change 8 (C-004, A-007)`
- **Validation**: Structural integrity OK | References OK (M-F5 resolves) | Contradictions OK

### Change 9: Task 3 control ambiguity, risk narrowed (M-F9)
- **Status**: Applied
- **Source**: Base F5; U-006
- **Target**: Base F5 -> M-F9
- **Before**: "can make the test unpassable".
- **After**: "could make the test unpassable if an implementer copied the ccsession-orca tests at :445 or :500, which the plan does not point to". Remedy, evidence, class Drift and severity minor unchanged.
- **Provenance tag**: `# Source: Base (original, modified) — Change 9 (U-006)`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 10: D08 line 23 trailing clause and stale citation (M-F10)
- **Status**: Applied
- **Source**: Variant A F4 (U-002); Round 2.5 probe (fault-finder) INV-021
- **Target**: New finding M-F10 after M-F9; `plan_ref: Task 8`, class Drift, severity minor
- **Before**: Did not exist in base.
- **After**: A-F4 claim and remedy kept, plus the stale `ccsession:78-83,93` citation (flags now at `ccsession:109-114, 124`) and the "update the line citation on the same line" clause. Evidence: D08:23, E01:21, PLAN:130, PLAN:135, `ccsession:109-114`, `ccsession:124`.
- **Provenance tag**: `# Source: Variant A F4 (U-002), with Round 2.5 probe (fault-finder) INV-021 folded in — merged per Change 10`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 11: B-F7 moved out of the findings list
- **Status**: Applied
- **Source**: Base F7; U-007
- **Target**: Card header comment
- **Before**: Finding F7 (Drift, minor, Constraints).
- **After**: Header comment with the plan's exact text ("Coverage-slice note (not a plan finding): ... record both as covered-by-plan."). No finding with that content remains.
- **Provenance tag**: `# Source: Base (original, modified) — Change 11 (U-007)`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 12: INV-022 as the verdict rationale
- **Status**: Applied
- **Source**: Round 2.5 probe (fault-finder) INV-022
- **Target**: Comment above `verdict`
- **Before**: None.
- **After**: The plan's exact comment text naming M-F1, M-F3 and M-F6.
- **Provenance tag**: `# Source: Round 2.5 probe (fault-finder), INV-022 — merged per Change 12`
- **Validation**: Structural integrity OK | References OK (M-F1, M-F3, M-F6 resolve) | Contradictions OK

### Change 13: Card-level fields
- **Status**: Applied
- **Source**: Plan Change 13; both variants
- **Target**: `verdict`, `self_confidence`, header, `not_checked`
- **Before**: `verdict: FAIL`, `self_confidence: 0.78`, base `calibration` block (0.87), 5 base `not_checked` items.
- **After**: `verdict: FAIL`; `self_confidence: 0.85` with a comment that it is orchestrator-set between 0.82 and 0.87 and not a calibration; header comment naming base, incorporated sources and plan. The base `calibration` block was not carried, because it calibrates reviewer 2's card alone and the plan sets the merged confidence; the two calibrated values are recorded in the comment. `not_checked`: 5 kept from B (the F6 reference renamed to M-F8), 2 kept from A narrowed, 2 added (M-F3's real-claude run; A-004 inheritance as an owner decision). Dropped as closed: A's `plugins/` mirror, `-k permissions` check, `case`/`:-` correctness, install-test header pinning, orca parametrize set. Required top-level keys placed first: `merge_method`, `adversarial_unavailable`, `convergence_score`, `convergence_caveat`, `base_variant`, `incorporated_variants`, `unresolved_conflicts`.
- **Provenance tag**: `# Source: Base (original, modified) — Change 13`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

## Post-Merge Validation

### Structural Integrity
- Valid YAML: OK (`yaml.safe_load` via `uv run --no-project --with pyyaml python -I`).
- Key order: OK. The first seven top-level keys are the required merge keys, followed by `verdict`, `self_confidence`, `findings`, `not_checked`.
- Schema: OK. All 10 findings have non-empty `id`, `claim`, `evidence`, `class`, `severity`, `plan_ref`, `recommended_change`. Every `class` is a taxonomy value (Regression or Drift); every `severity` is blocking or minor.
- Ordering: OK. Blocking M-F1, M-F2, M-F3, then minor M-F4 to M-F10, as in the plan's target table.
- Counts: 3 blocking / 7 minor, matching the plan's anchor table. Classes: Regression 4 (M-F1, M-F2, M-F5, M-F7), Drift 6.

### Internal References
- Total references: 17 (10 `plan_ref` values; 7 finding-id cross-references: M-F5 in M-F4 and M-F8; M-F1, M-F3, M-F6 in the verdict comment; M-F3 and M-F8 in `not_checked`).
- Resolved: 17. `plan_ref` values Task 1, Task 3, Task 5, Task 8, Task 9 and Constraints all exist as headings in the plan file; every referenced finding id exists in the card.
- Broken: 0.
- Citations: every `evidence` entry is a repo-relative `path:line` or `PLAN:<n>` taken from the base, Variant A, the probe or the plan, and each was re-read in this step.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Pairs checked: M-F4's launch-scoping option vs M-F5 (M-F5 constrains it, and M-F4 points to it); M-F5 vs M-F7 (both say the env file cannot set the variable for the current launch as written, and M-F5 shows only that moving the whole `case` would change that); M-F6 vs M-F7 (both say a `CC_CLAUDE_FLAGS` from the env file still replaces the flags); M-F1's claim (keeping line 109 alone fails the criterion) vs its remedy (keep line 109 and add the usage entry above it), which are consistent; M-F2 Regression vs M-F3 Drift on the same task (different defects).

## Summary
- Total changes planned: 13
- Successfully applied: 13
- Failed: 0
- Skipped: 0
- Notes (applied as written, recorded for the validator): Change 5 class written as `Regression`, with "latent" in the claim; Change 4 did not add INV-011's extra line anchors (the plan lists none); Change 13 dropped the base `calibration` block.
- Post-merge validation: PASS
