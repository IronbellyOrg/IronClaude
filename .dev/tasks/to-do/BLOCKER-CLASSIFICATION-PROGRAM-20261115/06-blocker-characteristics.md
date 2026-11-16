# Blocker characteristics (derived from the scored table)

Source: `05-scoring/consensus.md`. 82 of 318 historical findings reached a mean of 4.0 or higher on a 1-5 severity scale scored blind by three agents; the agreed blocking threshold was 4. All three scorers proposed it independently.

Status: draft 1. Derived from the 82 blockers by reading them (full list read on 2026-11-15) and counting keyword clusters. The classifier questions in `07-classifier/questions.md` start from the written rules (grading override, stoprule rubric, implement qa checklist) but were finalised after reading these rows, so the step 08 test is partly the table graded against itself: it measures consistency with the panel, not accuracy on unseen findings. This file is the data-driven view and checks that the written rules cover what the table calls a blocker.

## The test in one sentence

A finding blocks when someone who follows the text as written (an implementer, an executor, a gate, or a user) reaches a wrong or unsafe result that no later step in the same document would catch, and the result is not a matter of wording.

## Blocker characteristics

A finding is a blocker if at least one of K1 to K6 is true and the finding quotes the text and names the result. K7 and K8 are rarer and need the same two conditions.

| Id | Characteristic | Test a reader can apply | Rows in the 82 (only the keyword counts are counted; "about" means estimated by reading) | Typical examples |
|---|---|---|---|---|
| K1 | Safety boundary crossed | Following the text pushes to a protected branch, exposes a secret, acts on the wrong repository, lets an approval be bypassed, or overwrites or drops data | 10 of the 11 rows at a mean of 5.0 (the eleventh, F-B10-001, is K4 and K5), plus 8 push-rule rows (keyword count, overlaps the 5.0 rows); total not counted | F-B04-018 backtick push bypass; F-B01-010 job token left in git config; F-B07-023 coordinator reply approves a halted gate; F-B02-007 recovery merge drops task results |
| K2 | A required check cannot pass as written | The acceptance check needs a file, status or state that nothing in that phase produces, or two criteria cannot both hold | 13 on one defect (AC-0.4 in phase 0, keyword count) plus others not counted | F-B03-016, F-B05-018, F-B09-020 AC-0.4; F-B05-007 end-state criterion unreachable; F-B04-015 PASS impossible |
| K3 | The text contradicts a named contract, rule or existing behaviour | A correct input is rejected, or two quoted rules cannot both be followed | 17 on WC-4 (status vocabulary or contract location) plus 8 on WC-3 and approval gates (keyword counts, can overlap) | F-B05-023, F-B07-030, F-B10-030 status values; F-B08-010 contract path under a file |
| K4 | A required input, handle or target is missing or wrong | The step needs a value, file or branch that the text never supplies, or points at the wrong one | about 12 | F-B01-007, F-B04-004, F-B05-001 `target_sha` missing; F-B08-001 branch `integration` does not exist; F-B03-030 slot index; F-B10-006 missing positional so the command exits 2 |
| K5 | A failure is reported as success (fails open) | An empty, truncated, unknown or failed result is accepted as passing, or the item is still marked complete | about 6 | F-B06-009 mark complete on failed verification; F-B04-025 and F-B10-019 empty report read as success; F-B10-007 UNKNOWN read as PASS |
| K6 | A default performs an outward or unreviewed action against the stated mode | A mode, flag or switch is accepted but the dangerous default stays live | about 8 | F-B04-023, F-B09-029, F-B10-016, F-B08-013 flag lands before gates convert; F-B03-003 consent step still applies under unattended mode; F-B06-013 auto-fix applies items that need a human |
| K7 | Required work is missing from the plan or tasklist | A named required deliverable, command or action has no step | 3 | F-B02-016 four roadmap actions absent; F-B09-021 two commands in no phase |
| K8 | A loop or recursion has no bound | The text can run forever or recurse on its own output | 1 | F-B06-012 remediation emits its own terminal gate |

Cluster counts come from a keyword pass over the 82 descriptions. Six keyword clusters (AC-0.4 in phase 0, `--unattended` before gates convert, WC-4, WC-3 and approval gates, the git push classifier, `target_sha`) hit 54 matches and cover 43 distinct rows; 39 rows match none, so the table above is a reading of all 82, not a mechanical sort. The 82 blockers come from 55 distinct source documents. This matters for step 08: the table is heavy with repeats of a few defects, so agreement on the table partly measures agreement on those defects.

## What is not a blocker (scores 1.0 to 3.3)

| Id | Characteristic | Examples |
|---|---|---|
| N1 | Wording, naming, alias, label or count drift on a true statement | F-B01-031 two names for one thing (1.0); F-B07-007 "four" folders versus five (2.0) |
| N2 | A documentation line that misdescribes upstream behaviour, with no effect on what the code does | F-B02-009, F-B02-010 (2.0) |
| N3 | An edge case or a silent gap with a fail-safe or inferable result | F-B02-024 empty `--release ""`; F-B05-034 two probes neither included nor excluded (2.0) |
| N4 | A dependency note, graph line or flag omitted from an example, with the right behaviour recoverable from nearby text | F-B06-002, F-B08-031, F-B02-027 (2.0) |
| N5 | A test or doc update that the plan forgot, with the behaviour change itself correct | F-B07-009, F-B07-010 (2.0) |
| N6 | An ambiguity between two readings that give the same result | F-B08-032 (2.0) |

## Boundary cases the data shows (decide these in the rules, do not leave them to the scorer)

1. **Same defect, different score.** Variants of the AC-0.4 and WC-4 defects scored 4.0 in some documents and 3.33 in others (for example F-B10-028 at 3.33 and F-B06-018 at 3.67, against F-B05-018 at 4.0). Cause: the blind scorers saw the description only, and some descriptions state the failing consequence plainly and some do not. The classifier must read the stated consequence, not the topic.
2. **Fail-safe under-specification.** F-B05-001 (4.33), F-B04-004 (4.0), F-B06-008 (4.0) and F-B01-007 (4.33) are the same missing-parameter defect on a resume path. Downstream, a debate merged F-B05-001 and F-B06-008 as non-blocking (fail-safe), and the plan ground truth for F-B01-007 marks it non-blocking for implementation. Three scorers rated it blocking; the later adjudication did not. A rule is needed: a gap whose worst case is a safe halt is a follow-up, not a blocker (this is also the pragmatic output style's Medium class). K4 must therefore carry the condition "and the missing value cannot be recovered at run time without a wrong result".
3. **Verifier rejection.** F-B10-011 (4.33) was rejected by a verifier because the wrong outcome needed an unstated assumption. The classifier question for a wrong outcome must require that the result follows from the quoted text alone.
4. **Reviewer label versus consequence.** Reviewer markers (CRITICAL, MAJOR, `"blocking":true`, B-n headings) and the blind consequence score differ widely; for example the seven findings filed with `"blocking":true (severity MAJOR` all fall below the threshold. The label is not an input to the classifier.

## Rules distilled for the classifier (input to step 07)

1. Decide from the consequence in the text, never from the reviewer's label or the section it sits under.
2. A safety-boundary, secret-exposure, data-loss or wrong-target finding is never downgraded on a missing or unsettled answer (K1).
3. A required check that cannot pass, a quoted rule that cannot be followed, or a failure that reads as success is a blocker when the text alone shows it (K2, K3, K5).
4. A missing input or wrong target is a blocker only when running without it gives a wrong result; if the worst case is a visible halt, it is a follow-up (K4 with the fail-safe condition).
5. A default that acts outward or applies unreviewed changes against the stated mode is a blocker (K6).
6. Wording, naming, a wrong pointer on a true statement, a documentation line with no behaviour change, an inferable gap, and a suggestion to add something are never blockers (N1 to N6).
7. Many findings repeat across documents; the classifier scores each finding on its own text and the ledger groups repeats by cluster.

## Not verified

- The count of rows per characteristic is a keyword count plus reading, not a hand label of every row. A hand label of all 82 would take another pass.
- Whether the three scorers' blocking threshold (4) is right for the framework is not tested here; step 08 measures how a judge agrees with it. Reviewer-side outcomes (fixed later, downgraded later) are in the master table's Outcome column and are partly unknown.
