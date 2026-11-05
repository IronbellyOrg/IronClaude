# Diagnosability Tasklist
**Issue**: PR #359 round 2 hook misclassifications  **Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh  **Round**: 0 of 3  **re-run permitted**: yes  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: ironbelly/bare-python-hook-  **repro-venue-id**: bash .dev/troubleshoot/bug-pr-round-hook-findings-/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh

## Emitter search
emitters-found: 1 (src/superclaude/hooks/scripts/block-bare-python.sh:125 `print b`)
already-read-files: 1
usable-capture-routes: 1 (read-only scanner copy with a print at the chosen-word assignment; executed this run, trace-probe.out)

## Discriminator rows
core-rows=1, pack-rows=0, total-rows=1
| ID | role | claim | observable | probe | value-if-true | value-if-false | outcome mapping | provenance | state |
|---|---|---|---|---|---|---|---|---|---|
| D1 | core | the scanner never chooses python3 as the command word for the three inputs | cmdword= lines | trace-probe.sh | no python3 cmdword in any case | a python3 cmdword | true -> consistent; false -> refuted; empty capture -> unobserved | scanner source | observed: consistent (none / printf / echo) |

## Bracket
n/a

## Fix candidate
Proposal only (applied by sc-pr-submit-protocol): open the [[ context only for an unquoted, unescaped [[; give process substitution its own context that keeps the parent's command position and clears the redirect skip; scan backticks inside arithmetic.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
None required.

## Verification
D1 observed in trace-probe.out.

## Rollback
Nothing to roll back.

## Patch-round counter
discriminator-required: no; authoritative store not incremented.
