# Evidence Validation Report

**Report under validation**: REPORT.md.draft
**Timestamp**: 2026-11-23T19:32:28Z
**Total citations**: 17 (15 file/artifact spans, 2 command references)
**Verified**: 15
**Dropped**: 0
**Passed through (command, no reexec)**: 2
**Suggested report status**: success for citations/A-rules alone; does not lower existing hardening block.
**Review verdict (off-path diagnostic)**: FAIL (one blocking finding, three minor notes).

## Verified citations

| # | Type | Location | Verdict |
|---|---|---|---|
| 1 | file | commands.py:2145-2178 | verified: reduce, terminal state, summary, exit; no marker call |
| 2 | file | commands.py:2578-2599 | verified: resume has same omitted call |
| 3 | file | models.py:563-573 | verified: policy docstring and default true |
| 4 | file | commands.py:931-937 | verified: explicit flag true at935 |
| 5a | file | reduce.py:701-704 | verified: emit contract then return |
| 5b | file | reduce.py:383-440 | verified: separate marker writer |
| 6a | artifact | artifacts/foreground-check.json:1 | verified: done_exists=false and terminal |
| 6b | artifact | artifacts/foreground/return-contract.yaml:2 | verified: success |
| 7a | artifact | artifacts/resume-check.json:1 | verified: done_exists=false and terminal |
| 7b | artifact | artifacts/resume/return-contract.yaml:2 | verified: success |
| 8a | artifact | artifacts/foreground.stdout.txt:1 | verified exact |
| 8b | artifact | artifacts/resume.stdout.txt:1 | verified exact, skipped3 redispatched0 |
| 9 | artifact | artifacts/import-paths.txt:1-2 | verified this worktree's source |
| 10a | artifact | artifacts/baseline-tests.txt:7 | verified25 passed, existing tests only |
| 10b | artifact | artifacts/negative-witness.txt:3-5 | verified exit1 and AssertionError |

## Dropped citations

None.

## Passed-through citations (command, allow_command_reexec=false)

1. Existing pytest invocation in baseline-tests.txt:1: recorded result verified, no re-execution.
2. Marker-presence oracle in negative-witness.txt:2: recorded failure verified, no re-execution.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | none | none | Missing-file fact captured in both raw check JSONs; calibrated1.00 |
| A2 | skipped | none | none | input absent: diff_path=null; no measurement/enabling rows |
| A3 | no | none | none | draftDate19:31:01 precedes supplied draftmtime19:32:07, not midnight |
| A4 | no | none | none | blocked is an allowed hardening verdict |
| A5 | skipped | none | none | candidate-fixes.md absent; no consensus claim |
| A6 | no | none | none | no discriminator reference values |
| A7 | no | none | none | zero producer rows, no pending-producers locus |
| A8 | no | none | none | local same-shell failing arm, not CI |
| A9 | no | none | none | no reference value/arm capture |
| A10 | no | none | none | capability-verdict=n/a, not blocked |

## Off-path diagnostic review

Checked all15 cited spans independently, skill Waves4.5/5/6, runtime-entrypoint-verification, hardening-output-contract and pipeline-hardening-closure refs, plus runtime/ledger/applicability/effective-input cards. Product diagnosis is supported: the omitted calls and scoped real CLI artifact failures match. No command executed or file modified by reviewer.

### Blocking finding B1

The claimed workflow conflict and assertion that the protocol mandates report status blocked are not established as unconditional facts. Consequence: these claims withhold the planning offer and ask human resolution on a possibly parent-chosen interpretation.

Verified: skill Wave6 requires --fix, report success and user acceptance. Ambiguous: skill Wave4.5 names a negative witness, while the runtime ref schema requires a positive witness and its pairing sentence requires fix-applied PASS. The ref does not define a pending state for diagnosis before a fix. No explicit rule maps ordinary HC FAIL/hardening blocked to diagnostic reportstatus blocked; only blocked-on-authorization expressly mandates it. Downstream contract line54 instead names success_with_hardening_blocker. A rationalized HC1 N/A could instead produce advisory under truth-table row6.

Required correction: present this as unresolved protocol ambiguity, cite both sides, state the conservative chosen HC1 FAIL/reportblocked interpretation, and acknowledge the advisory alternative. Do not change evidence or product diagnosis, invent a repair, or silently clear closure proof.

### Minor notes

M1 (citation form): detached-child statement is source-only but lacks a direct evidence citation; supported indirectly by ledger, reviewer did not read that source span. Cite or soften.
M2 (provenance cross-reference): full command/exit provenance is delegated to tier1-observation.md, not read in this review; raw cited captures verified.
M3 (pending-state bookkeeping): Audit/HC5 still says validation pending. Update after receipt; HC5 remains FAIL while blocking B1 is unresolved, and recheck the correction.

## Notes

Product hardening closure remains blocked/NOT PROVEN for absent positive witness; this review does not lift or certify it. Existing evidence-validation.md and REPORT.md were listed but not read or treated as inputs. This returned report must replace the stub, not be substituted by it. Zero citation drops do not override the independent blocking substantive review finding.
