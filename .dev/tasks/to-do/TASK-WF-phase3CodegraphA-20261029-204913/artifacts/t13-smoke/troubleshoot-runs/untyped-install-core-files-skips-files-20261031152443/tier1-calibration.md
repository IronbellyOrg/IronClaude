# Calibration Report

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/troubleshoot/untyped-install-core-files-skips-files-20261031152443/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-10-31T15:27:29Z

## Per-dimension scores

Declared on the card: `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: AFFIRM`. The claim text describes a plain conditional branch, not dynamic control flow, so I did not treat it as a misdeclared `static_defect`.

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | I read every cited location and each snippet matches. `install_core.py:66-68` is `if dest_file.exists() and not force:` then `skipped.append(src_file.name)` then `continue`. Lines 83-88 build the "Skipped N existing files (use --force to overwrite)" message and list each name. `installation.md:263` is the `--force` row, "Overwrite existing files". `test_how_we_work_install.py:53-75` is `test_install_never_touches_existing_files_without_force`, which asserts byte equality of seeded files. |
| Runtime check | 0.0 | The cross-tab for (runtime_behavior, source_static) gives 0.0. The card has no executed reproducer, no captured output and no runnable command. It cites a real test, but declares it "not-run". Under the cross-tab, the 0.5 override needs a runnable command in the card, and there is none. Borderline: the rubric's 0.5 anchor also mentions "cites a test that exists but was not exercised". If you read that as 0.5, the result is 0.58 and the verdict still escalates on signals (see Notes). |
| Symptom coverage | 0.5 | The reported symptom is only "install_core_files skips files". The skip branch explains one way a skip happens. The card admits no filenames, invocation or message were supplied (Grounding gaps). It also leaves other skip causes open: copy failures and the `*.md`-only glob (`install_core.py:54`). |
| Reproducibility fit | 0.5 | The branch is deterministic (`install_core.py:66-68`), but no reproducer was attempted. The card says "no reproducer". |
| Fix directness | 0.0 | The card says "No causal fix established; no files to change." |
| Domain coherence | 1.0 | Installer only. |

Adjustments from the structural assertions: C3b caps Runtime check at ≤ 0.5. It is already 0.0, so nothing changes. No other C-rule changed a dimension.

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.50 | (1.0 + 0.0 + 0.5 + 0.5 + 0.0 + 1.0) / 6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.30 | binding |
| gated_min | 0.30 | min(0.50, 1.30, 0.30) |
| verdict_cap | 0.84 | M3a applies (runtime_behavior, runtime_check &lt; 1.0, AFFIRM). Not binding, because 0.30 &lt; 0.84. |
| **calibrated** | 0.30 | final; no structural cap lowers it further |
| spot_check_unverifiable | none | No remote URLs cited. |
| structural_flags | locus_unknown | C3b fired. C1, C2, C3, C4, C5, C6 and C7 did not fire. C8 was skipped (input absent). |

## Confidence

- **Self-reported (in card)**: 0.30. I read it but did not use it as input.
- **Calibrated (this report)**: 0.30
- **Formula applied**: `min(0.50, 1.30, 0.30) = 0.30`. The AFFIRM cap of 0.84 leaves it at 0.30. The only fired cap, C3b, applies to Runtime check (≤ 0.5, already 0.0). No 0.3 or 0.5 calibrated cap fired. Final is 0.30.
- **Delta**: 0.00. The card's own dimension scores match mine exactly, and its 0.30 is the Runtime-check gate (0.0 + 0.30). The card already describes itself as a conditional explanation, so there is no overclaim to correct.

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none` (suppressed by the hard stop below)
- **Rubric rule fired**: Rule 1, hard stops: "`--depth quick` set → STOP at Tier 1." (`flags_context` has depth:quick and no_escalate:false.) C1 did not fire, so nothing forces ESCALATE.
- **Execution restriction**: `--depth quick` → STOP at Tier 1. Without that restriction, the signal rules would have recommended ESCALATE for two reasons. First, `low_confidence`: 0.30 is below 0.85. Second, `source_only_dynamic_claim`: runtime_behavior with runtime_check 0.0, which is below 0.5. These signals did not fire: `multi_domain` (Domain coherence is 1.0), `intermittent` (not described), `not_reproducible` (Reproducibility is 0.5, not 0.0), `security_caution` (type auto), and `split_pending` (a single Tier 1 card cannot trigger it). The investigation should remain `partial` and low-confidence. The STOP reflects the depth flag, not any evidence that the cause is settled.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | The headline (card:1) and Claim (card:13) assert no definite enum token and call it "one conditional explanation, not an established cause". Calibrated 0.30 is under 0.50, but the token condition fails. |
| C2 | no | — | — | card:34 says no failing-run evidence "establishes or excludes" copy failures, so no enum is excluded. |
| C3 | no | — | — | card:32 says "No passing arm claimed". The control row at diagnosability-tasklist.md:18 records CONTROL-PROOF=unknown and no comparator. No control arm is cited. Even if it fired, Symptom coverage is already 0.5. |
| C3b | yes | `locus_unknown` | Runtime check ≤ 0.5. Already 0.0, so no numeric change. | card:11 `runs-in=unknown`; execution-locus.md:3 `RUN-SITE: ... @ unknown`; execution-locus.md:4 `SAME-ENV: unknown` |
| C4 | no | — | — | The capture row (diagnosability-tasklist.md:17) has a true prediction, a justified-unknown false prediction ("other failure mechanisms not identified") and an outcome mapping. The control row (line 18) has justified unknowns and an "Inconclusive" mapping. The enabling task (line 27) links measurement `capture` and gives verification and rollback. Its site matches main.py:178-179, which I read. |
| C5 | no | — | — | Card timestamp 2026-10-31T15:24:43Z (card:4) is earlier than card_mtime 15:27:29Z, and it is not T00:00:00Z. |
| C6 | no | — | — | The headline asserts no numeric threshold or bracket. diagnosability-tasklist.md:19-20 says "Not triggered: no numeric limit supplied". The sibling bracket.md does not exist, which is consistent with that. |
| C7 | no | — | — | card:36 says no "environment-property causal claim established". Environment appears only as a missing input. |
| C8 | skipped | — | — | input absent: behaviour_definitions_path (null). card:19 also says no external primitive behavior is asserted. |

## Notes

- **Spot-check results.** Every citation in the card verified at the stated lines. Three citations from the tasklist also verified. First, `install_core.py:101` is the `return success, "\n".join(messages)` line. Second, the skip-message lines 83-88 match. Third, the `main.py:178-179` pair is `core_success, core_message = install_core_files(force=force)` followed by `click.echo(core_message)`. The card's "Alternatives considered" claims also hold: copy failures are collected in `failed` (`install_core.py:70-74`), and the source is selected by `glob("*.md")` (line 54).
- **Test citation.** The test exists and asserts byte preservation for `install_core_files` and `install_commands` with `force=False`. It supports the preservation contract in general, not the user's specific run. The card correctly declares it not-run, and I did not run it (read-only).
- **Runtime check sensitivity.** I scored 0.0 on the cross-tab. If the parent prefers 0.5 for the existing-but-not-run test, the numbers become: mean 0.58, M2 0.80, cap 0.84, calibrated 0.58, which still escalates on `low_confidence`. Neither reading changes the STOP, which comes from depth quick.
- **Card structure.** The card has no YAML frontmatter. The class fields are bold header lines and are parsed as declared. `consistency_with_docs: aligned` appears twice (card:9-10), which is harmless. `input_absent: behaviour_definitions_path`. No input is absent for `now_iso`, `card_mtime`, `tasklist_path` or `locus_path`.
- **bracket.md.** Reading `bracket.md` beside the tasklist returned file-not-found. C6 did not need it, because no bracket is asserted.
- **Capture gap.** This is a restatement of the card's own gap, not a new finding. The only thing that would move the confidence is the original command, `force` value and returned message (tasklist rows `capture` and `control`). No such artifact was supplied.
- **No files written.** The parent persists this report to /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/troubleshoot/untyped-install-core-files-skips-files-20261031152443/tier1-calibration.md.
