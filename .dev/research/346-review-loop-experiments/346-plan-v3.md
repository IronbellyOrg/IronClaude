# Issue #346: revised remediation plan (v3)

Revised 2026-11-09. Changes from v2: folds in the phase 4/5 experiment evidence from `ironbelly/exp346-p1-logs` (`.dev/experiments/346-validation/`, paths below relative to it). Replaces v2's planned baseline-vs-treatment experiment, which has in effect already been run. The fixes that need no experiment are split out and shipped first.

## Decision

Ship three things, in this order:

1. **Product fixes that need no experiment.** These remove the effective prompts that still override #427.
2. **A small extension to the spec-panel Review Loop**, built on #427.
3. **A replicated validation run**, only if the owner explicitly authorizes live runs.

Retiring spec-panel (D1) stays a separate decision. No variant is merged.

## What the experiments settled (no need to re-test)

### Setup
- **One scenario.** S1, the 57,763 B Orca worker-contract spec, run through 3 reviews and 2 fix cycles. The other incidents never call spec-panel (`DECISIONS.md:41-42`).
- **Arms.** Control (pre-#427) against exact #427, 2+2 replicates. Then #427 with `--re-review/--baseline` (2 runs). Then five variants; three of them completed one loop each.
- **Tested the shipped text.** The #427 Review Loop the experiments ran is byte-identical to master `spec-panel.md:256-264`.

### Results

| Finding | Evidence |
|---|---|
| **#427 roughly halves document growth.** Mean growth fell from 63.5% to 29.7%, and every #427 run grew less than every control run. This is the one robust effect. | `phase4/AB-REPORT.md:12-24` |
| **#427 alone does not converge.** No arm reached PASS. The last-round blocking count was 5.5 against a control of 6, with #427 plus flags at 3.5. The differences are within run-to-run noise. | `phase5/FINAL-REPORT.md:75`, `:94-107` |
| **New findings still land on just-fixed text.** Under #427, 89% (review 2) and 100% (review 3) of new findings sit on lines changed by the previous fix (`origin=changed`). | `phase4/AB-REPORT.md:30` |
| **Briefs override the command.** Every arm kept the original brief clauses "assume defects remain" and "any finding of any severity is FAIL", contradicting #427 bullet 7. Revisers acted on 7 and then 8 MINOR findings. Ponytail ended FAIL only because of a carried MINOR. | `DECISIONS.md:74` item 2; `phase2/S1/briefs/task-text/T07…`, `T09…`; `phase5/FINAL-REPORT.md:150-152` |
| **A restricted re-review misses real defects.** Diffgate grew least (10.3%), but a full-document audit afterwards found 4 more MAJOR findings, and the ledger sweep found 9. | `phase5/FINAL-REPORT.md:103-105`, `:120` |
| **The user command copy shadows the project copy.** `make sync-dev` cannot activate a changed command, so stale installed copies are the real risk. | `DECISIONS.md:46` |
| **No variant is a validated winner.** Each variant has one unreplicated run. Ponytail's reviewer model switched to gpt-6.1-sol and its parser emitted an invalid zero. Stoprule's provenance check was invalid. Minfix's build halted. | `phase5/FINAL-REPORT.md:101-107`, `:197-204` |

### Not tested by anyone
- Seeded or deletion-induced defects.
- A clean-document or minor-only control.
- Interrupt/resume.
- A second document type, such as PRD/TDD loops.
- Any arm without the "any severity is FAIL" brief.

### Caveat on the noise floor
The low control run (ctl-r2) read the finished answer in `origin/master` (`phase4/ARMB-REPORT.md:83`). Count comparisons at n=2 cannot detect effects smaller than about 4 findings.

## Track 1: product fixes (ship as one PR, no experiment needed)

These remove the effective prompts the evidence shows overriding #427. Each edit gets a text-contract test in the existing `tests/` style.

| # | Edit (master @ 933cf3a4) | Change |
|---|---|---|
| 1a | `output-styles/pragmatic.md:221-222` | Replace "assume mistakes" and "zero findings is suspect" with: a review reports concrete defects with evidence; a zero-finding result is valid with a short statement of what was checked; no quota. |
| 1b | `output-styles/pragmatic.md:232-233` | State that deleting or narrowing redundant text is allowed when requirements still hold, and that "no simplified versions" means no stubs, not no deletions. |
| 1c | `skills/task/SKILL.md:233`, `:430` | Remove "Assume at least N errors". Keep the requirement to state what was checked. |
| 1d | `skills/sc-cli-portify-protocol/SKILL.md:289` | Replace the "additive-only" rule with the #427 reviser contract (revise only text a blocking finding names). |
| 1e | `core/HOW-WE-WORK.md` near `:65` | Add a paste-ready review brief and revise brief that defer to the command's Review Loop. The brief must not contain any-severity FAIL, defect quotas, or "apply all findings". This is the brief the experiments show is missing. |
| 1f | `cli/install_user_setup.py:140-152` | Port the #419 kept-file-differs warning (`install_core.py:94-101`) to output styles and to commands. Make `superclaude update` (force) back up a differing file before overwriting it. |
| 1g | `commands/spec-panel.md:313`, `:328-329` | Replace "minimum 6 rows per guard" with "one row per input class that applies". A GAP is blocking only when it names a concrete wrong outcome, the same test as MAJOR in bullet 2. Keep FR-10 (synthesis-blocking gate). |

Run `make sync-dev` and `make verify-sync`. Before committing, run the `grep 'src/superclaude'` check from CLAUDE.md. Budget about 4 hours.

## Track 2: smallest extension of the #427 Review Loop

Edit `spec-panel.md:256-264` in place. No scripts, parsers or new commands. Every bullet below responds to an observed failure; none has been validated yet.

1. **Precedence (bullet 7).** A brief cannot fail a minor finding or authorize a minor edit, including through "apply all findings". The report names any brief clause it overrode. *Observed:* the T07/T09 briefs, and the ponytail FAIL on a MINOR.
2. **Identity (bullet 5).** Prior blocking findings keep their IDs and get exactly one disposition: `resolved`, `open`, `regressed`, `deferred` or `withdrawn`. `deferred` and `withdrawn` count as open for the verdict and for escalation. *Observed:* count drift between the ledger and diffgate.
3. **Fail closed (bullet 3).** If the resolution table or the verdict line is missing or ambiguous, the verdict is FAIL. A zero finding count is never inferred. *Observed:* ponytail's invalid parsed zero.
4. **Coverage line.** A re-review PASS reads `scoped PASS: changed lines + prior blockers`. Whole-document assurance needs a separate, labelled first review. Any blocker that review finds goes to escalation, never to a fourth review. *Observed:* the diffgate and ledger audits.
5. **Reviser (bullet 6).** Prefer deleting or narrowing over adding. Report gross bytes added and deleted per finding ID, not just net size. No numeric budget. *Observed:* diffgate's growth was hidden inside long lines that already existed; minfix's budget was never measured.
6. **Provenance (bullet 1).** The report header records the baseline and candidate SHA-256, the command version and the actual reviewer model. *Observed:* ponytail's silent model switch.
7. **Cap (bullet 4).** No edits between fix 2 and review 3. Any necessity audit only reports. *This keeps the 2-fix cap intact.*

Add text-contract tests for each bullet. Budget about 3 hours.

## Track 3: validation (only with explicit owner authorization)

Live runs are outside the current authorization, so the first step is a bounded permission request. If granted:

- **Arms.**
  1. #427 with the original briefs (existing data, reused).
  2. #427 with the Track 1e briefs: the single change is the brief.
  3. Arm 2 plus Track 2: the single change is the contract.
- **Design.**
  - At least 3 replicates per arm, run concurrently.
  - No access to `origin/master`, so no answer exposure.
  - Model continuity verified.
  - The same post-loop whole-document audit in every arm.
  - Additive command names, so arms can run in parallel (`phase4/AB-REPORT.md:47`).
- **Added cases.**
  - Seeded severe defects, including one introduced by a deletion and one regressing a prior PASS.
  - A clean document.
  - A minor-only document.
  - One interrupt/resume.
  - One PRD/TDD document.
- **Success.**
  - The last-round blocking count improves by more than the within-arm spread.
  - Growth is no worse than arm 1.
  - Every seeded severe defect is reported.
  - Clean and minor-only documents PASS within 3 reviews.
- **Stop rule.** Publish whatever was learned once the authorized run budget is spent. No automatic continuation.

## Separate decisions (unchanged in substance)

- **D1, retire the spec-panel family.** Deferred. The evidence shows no variant winning and no harm unique to the panel; the minor-only FAIL came from briefs.
- **D2, RF reviewer floors** (`task/SKILL.md:121-122`, `:194`). Follow-up. The quota part moves into Track 1c.
- **D3, bound correction.** Covered by #427 and Track 2.7.
- **D4, read-only reviewers and report writes.** This is #465; out of scope.

## Notes on the DESIGN-BRIEF

`phase5/DESIGN-BRIEF.md` points at the same target as Track 2: the smallest extension of #427. Three problems:

- **It is stale.** It calls FINAL-REPORT-QA "pending" (`:7`), but QA passed on fidelity (`FINAL-REPORT.md:53`).
- **It requires a live `sc:design` run** (`:28`), which conflicts with the no-live-runs constraint.
- **It invites the growth it warns against.** "Fail-closed parsing… asynchronous transport" (`:19`) presumes the script machinery that `:15` rejects.

It also does not define "owner's carry-forward accounting" (`:16`). Track 2 can stand in for its REFACTOR-SPEC as prose, without the 06 template.

## Open items carried forward

- FINAL-REPORT's stale bundle checksum inventory (`:252`) and its history row still marked "pending" (`:257`).
- The paused repeats.
- The framework gap that a dev checkout cannot exercise a changed command (`DECISIONS.md:46`). Worth its own issue.
