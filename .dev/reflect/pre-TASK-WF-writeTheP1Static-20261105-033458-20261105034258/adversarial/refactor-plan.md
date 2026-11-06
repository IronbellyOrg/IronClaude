# Refactor Plan (merge of reviewer cards into one review card)

Base: V3 (reviewer 3 card). Merge target: `merged-review-card.md` in the reflect output folder. Plan under review is referred to as `plan:N` (`.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md`). Severity scale of the merged card: blocking (a real defect: wrong behaviour or a missing required deliverable) and minor. Every debate "should-fix" is blocking on this scale because each leaves a required behaviour unfulfillable or a check that fails on a correct run; every debate "minor" stays minor.

## Changes to make in the base

| # | Source | Change | Merged id | Severity |
|---|---|---|---|---|
| 1 | V1 R1-01 + V3 R3-03 (base) | Merge into one finding: graph and impact skills have closed flag tables and write the contract only via `--output-dir` (graph `SKILL.md:64`, `:85`; impact step 10 `:49`, write scope `:182`); Tasks 4 and 5 must add the two flag rows, edit G-O / step 10 / the "(only with `--output-dir`)" heading / the write-scope sentence, and say where `impact.md` lands and that the worker contract at `<report-dir>` lists it in `artifacts`. Drop V1's blocking label and its impact sub-claim. | MF-01 | blocking |
| 2 | V1 R1-13 | New finding: graph `init` refusal must be a skill STOP row (positional `init` with `--unattended` gives `blocked`, mapped to `failed`), not a step after Init, because `graph.md:40` runs the skill first and the Init steps start after its preflight (`graph.md:46-48`). | MF-02 | blocking |
| 3 | V3 R3-02 (base) + V1 R1-02 + V3 R3-09 + probe INV-3 | init-lite: Activation bullets for both flags; the skill keeps both off the CLI call and writes the contract itself on every outcome including `--dry-run`; "except" line next to `init-lite.md:94`. | MF-03 | blocking |
| 4 | V3 R3-01 (base) + V1 R1-05 | Task 15 path-list check: scope to `git status --short --untracked-files=all -- src tests plugins`, or compare against a Task 1 baseline. | MF-04 | blocking |
| 5 | V3 R3-04 (base) + V1 R1-03 | Task 14 nested test: per-command data field `UNATTENDED_EXPECT[cmd]["nested"]` (brainstorm `[analyze, adversarial]`, workflow empty). | MF-05 | blocking |
| 6 | Probe INV-1 | brainstorm: use the passed dir exactly under `--unattended` (no `-N` suffix), refuse a dir that already holds a `return-contract.yaml`, write a `failed` worker contract on every STOP. | MF-06 | blocking |
| 7 | Probe INV-2 | `--report-dir` gets the same path rules as the command's own dir flag; a rejected or unwritable report dir is "no report dir known" (chat-only refusal). | MF-07 | blocking |
| 8 | Probe INV-5 | Decision D-P1-12: consent steps in test, analyze, design under `--unattended`. | MF-08 | blocking |
| 9 | Probe INV-4 + INV-6 | brainstorm: skip Wave 0 step 7 under `--unattended`; add `handoff-routing.md` to Task 3 with an `--unattended` block; refuse `-i` and the `=` spellings. | MF-09 | minor (probe MEDIUM; edit is small and applied with MF-06) |
| 10 | V3 R3-10 + V1 R1-04 | Python form of Check SCAN regex plus a negative case. | MF-10 | minor |
| 11 | V3 R3-08 + V2 R2-03 | "first `## Boundaries` heading" wording in the skeleton. | MF-11 | minor |
| 12 | V3 R3-06 + V2 R2-04 | Drop `tests/test_cleanup_audit_structure.py` from Task 6; fix count (six). | MF-12 | minor |
| 13 | V1 R1-07 + V2 R2-05 | Reword D-P1-1's lead-in; coordinator ratifies in the Task 15 report. | MF-13 | minor |
| 14 | V3 R3-05 + V1 R1-12 | Define a lint pass: no new ERROR or ruff finding; new WARN lines recorded. | MF-14 | minor |
| 15 | V1 R1-10 | Name `-i` and `-o` in the adversarial section. | MF-15 | minor |
| 16 | V3 R3-07 | Task 9: apply the `--output` retirement rule and the `E-MISSING-DIR` ban to the skill and ref edits. | MF-16 | minor |
| 17 | V2 R2-06 | Decision D-P1-11 for the init-lite invariant-2 extension. | MF-17 | minor |
| 18 | V2 R2-07 | One Task 15 inventory line naming plugin command copies left stale. | MF-18 | minor |
| 19 | V2 R2-01 + calibrator | Task 11: frontmatter keys and values byte-for-byte unchanged, including trailing spaces on `business-panel.md:6`. | MF-19 | minor |
| 20 | V1 R1-11 | Note only: the stale table in `WORKER-CONTRACT.md` is outside this plan's files. | MF-20 | minor |

## Changes not made (debate-rejected)

R1-06 (the downgrade of brainstorm nesting; `spec:142` says "from P2" but the plan discloses D-P1-4, left as an owner question). R1-09 (unconfirmed, matrix not read). R1-01's impact sub-claim (wrong: `--output-dir` has a default at `impact SKILL.md:29` and step 10 always writes). R2-01's "no fix needed" conclusion. R3-06's "seven" count. R3-08 as should-fix (stays minor). The "bad flags blocked" wording in the graph and impact tables (no STOP column lists an unknown-flag stop).

## Verdict derivation

Reviewer verdicts FAIL (V1), PARTIAL (V2), PARTIAL (V3); merged verdict PARTIAL: eight blocking findings (MF-01 to MF-08), each with a concrete plan edit and none structural to the plan's design; twelve minor notes.
