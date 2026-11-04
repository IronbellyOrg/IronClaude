# Diagnosability Tasklist
**Issue**: PR #359 round 1 hook misclassifications  **Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh  **Round**: 0 of 3  **re-run permitted**: yes  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: ironbelly/bare-python-hook-357  **repro-venue-id**: bash .dev/troubleshoot/bug-pr-bare-python-hook-findings-/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh

## Emitter search
emitters-found: 1 (src/superclaude/hooks/scripts/block-bare-python.sh:111 `print b`)
already-read-files: 1
usable-capture-routes: 1 (a copy of the scanner text, extracted read-only by trace-probe.sh, with one added print at the `cmd[o] = b` assignment; the hook file is not modified)
Route executed this run (re-run permitted: yes, same-shell): output in trace-probe.out and tier1-observation.md.

## Discriminator rows
core-rows=1, pack-rows=0, total-rows=1
| ID | role | claim | observable | probe | value-if-true | value-if-false | outcome mapping | provenance | state |
|---|---|---|---|---|---|---|---|---|---|
| D1 | core | scanner picks the wrong command word for each symptom input | cmdword= lines | trace-probe.sh | 160ython3 / 30 / [[,python | python3 / python3 / [[ only | match true -> consistent; match false -> refuted; empty -> unobserved | src lines 101, 190-191, 206 | observed: consistent (160ython3 / 30 / [[,python) |

## Bracket
n/a (no bracket trigger)

## Fix candidate
Proposal only (applied by the caller sc-pr-submit-protocol under its own fix gate): decode ANSI-C escapes in qchar; consume long-option and clustered short-option arguments in endword; treat `[[ ... ]]` as a test context with no command words.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
None required: the only measurement (D1) ran through a read-only copy outside production source.

## Verification
D1 observed in trace-probe.out.

## Rollback
Nothing to roll back (no instrumentation added to any file).

## Patch-round counter
discriminator-required: no, so the authoritative store .dev/troubleshoot/diagnosability-rounds.json was not incremented.
