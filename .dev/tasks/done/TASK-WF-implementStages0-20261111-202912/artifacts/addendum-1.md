# Addendum 1: calibration source in the shadow steps (user-authorized scope change after FINAL review 1)

Trigger: FINAL review 1 (`./final-review-1.md`) returned `issues`: `SKILL.md` shadow step 5 (added by Task 19) said the legacy blind calibration "embeds a `calibration:` block in each card". A blind check of the recorded runs (37 runs, 102 cards) found the layouts mixed: 21 runs keep reviewer calibration only in a separate file, 10 runs embed a real block, 2 use a variant, 4 have none. The user then asked for the revised fix and for an adversarial debate on whether `review cluster` should read the recorded layouts directly, adding code and a plan change only if the return is high.

## Debate (opponent: a separate sub-agent argued against; the orchestrator argued for)

Facts both sides verified on disk:

- `./stage0a-report.md:370-376`: of 689 recorded findings, 0 have a numeric confidence (embedded 0 of 271, sidecar 0 of 347, none 0 of 71). Older `per_finding` entries are words such as `confirmed` or `grounded`.
- Numeric per-finding confidences exist in one of 74 `pre-*` runs: the newest (`.dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203517/artifacts/reviewer-calibration.yaml:9,14,19`), keyed `F1...`, while that run's cards name findings `R1-F1...`: an id mismatch that no file format fixes.
- `confidence-calibrator` returns one score per card, so per-finding numbers exist only when the brief asks for them.
- `cluster_agreement` is telemetry; no stage exit or entry test uses it.

Verdicts:

- Multi-layout reader in `review cluster`: rejected. About 130 lines and 10 tests would recover 0 of 689 recorded confidences and feed a value that decides nothing.
- Narrow reader (YAML or the shared `cards:` sidecar shape): rejected by the opponent on two grounds that the orchestrator checked and accepted: the ids do not match on the one real file, so it would join 0 findings, and no skill text prescribes that shared file (it was one run's improvisation), so it would turn an improvisation into a second sanctioned layout. It also changes `--calibration` from a loud failure on YAML input to a silent non-match.
- Adopted (high return, about 6 lines of code and 3 tests): `review cluster` reports how many clustered findings found a numeric confidence (`calibrated_findings: n/m` on stdout and `calibration_coverage` in `clusters.json`/`clusters_kept.json`). An id mismatch under any layout now shows as `0/m` instead of a silent empty `cluster_agreement`.
- Adopted (text only): `SKILL.md` shadow step 5 stops claiming the legacy card embeds a block; the orchestrator writes `panel/cards/reviewer-N.md` with the findings block plus a `calibration:`/`per_finding:` block keyed by the exact finding ids, with numeric confidences only (none invented from verdict words or copied from the card score); step 6 reads `calibrated_findings` and records `calibration_coverage`; section 9.2 gains `calibration_coverage`.

## Scope and plan

- Files changed after the FINAL: `src/superclaude/cli/review/cluster_cmd.py` and `tests/review/test_review_cluster_cmd.py` (Task 12 deliverables), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (Task 19 deliverable).
- The plan file `./TASK-WF-implementStages0-20261111-202912.md` is pinned by hash in `progress.md` and is not changed (a change would stop the run with `E-PLAN-CHANGED`). This addendum is the record of the added scope; the fresh FINAL reviewer is told to check it.
- No task is reopened in the ledger; the per-task `complete` lines stay as recorded.
- Out of scope, not done: changing the `confidence-calibrator` agent file itself (the shadow steps now say the calibrator brief asks for one numeric confidence per finding id); a word-to-number table; a reader for the recorded sidecar layouts.

## Follow-up after FINAL review 2 (`./final-review-2.md`)

FINAL review 2 found one more false statement in the text this addendum introduced (F2.1: a coverage below m was attributed only to id mismatches). `SKILL.md` shadow steps 5 and 6 and the section 9.2 line were corrected: a coverage of 0 or below m means ids that do not match, no calibration given, or findings the calibrator left unscored; the orchestrator compares the ids and fixes them only when they differ. Step 5 now also lists the `persona:`/`model_class:`/`model:` header lines at the top of each panel card (F2.2) and says that in shadow mode one instruction line is added to the calibrator brief while the card-level score still feeds the rubric and the debate as in section 11.3 (F2.3). F2.4 (a mismatched line number in the T8 evidence) is left as recorded; the ledger is append-only and the criteria hold at the lines listed in `./final-review-2.md`.

## Follow-up after FINAL review 3 (`./final-review-3.md`)

FINAL review 3 found two more false consequence statements (F3.1 in `SKILL.md` step 6 and F3.2 in a `cluster_cmd.py` comment: with no blocking cluster `cluster_agreement` is 1.0 whatever the coverage). Both were corrected. The non-blocking findings were also fixed in the text: `kept-ids.txt` now takes one `reviewer-<N>:<finding id>` per line (F3.3); step 1 states that `review panel resolve` always resolves the template's full list, so a run with `--reviewers 2` records `panel_parity` false and shadow measurement runs use the default reviewer count (F3.4); step 5 says the legacy calibration is unchanged except for the one brief line (F3.5). F3.6 (no recorded owner go-ahead after Task 4's stop) is unchanged; the user's "conitnue" message after the stop is the go-ahead and it is recorded in this addendum rather than in the append-only ledger.

## Follow-up after FINAL review 4 (`./final-review-4.md`)

FINAL review 4 found five more false consequence statements in the text this addendum introduced (F4.1 to F4.5). Four rounds of review each found new ones because each correction added a new, more specific claim. The corrections of this round remove the consequence claims instead of refining them: step 1 says only that `review panel resolve` has no reviewer-count option and does not apply `N_eff`, and that `panel_parity` records whether the legacy run and the resolution differ; step 6 lists causes of a low coverage with "include" and makes no statement about what `cluster_agreement` becomes; the section 9.2 line says "0/m means no clustered finding was matched to a numeric calibration"; the `cluster_cmd.py` comment says the report only counts; the docstring says the sidecar overrides each reviewer "it names with a non-empty mapping".

## Follow-up after FINAL review 5 (`./final-review-5.md`)

FINAL review 5 found three more inaccurate statements, all in comments, docstrings or help text (F5.1 the `advance` help for `--stage published`, F5.2 the order in which `cluster_cmd.py` looks for calibration blocks, F5.3 "numeric" for a value outside 0 to 1 in the section 9.2 line). Each was reworded to say exactly what the code does. No acceptance criterion and no code behaviour changed.
