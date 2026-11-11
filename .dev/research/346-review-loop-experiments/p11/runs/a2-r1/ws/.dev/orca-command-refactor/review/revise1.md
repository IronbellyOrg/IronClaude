revise: 1 of 3

# Revision 1: `orca-worker-contract-spec.md`

Scope: blocking findings B-1 and B-2 of `.dev/orca-command-refactor/review/round1.md:92-102,207-211`. Medium and minor findings were left alone. No PASS is awarded here. `SPEC:N` = line N of the revised spec. Spec-panel not run.

## Byte accounting (spec file)

| | Bytes |
|---|---|
| Before | 57763 |
| After | 58099 |
| Net | +336 |

Per finding id (a replaced span counts fully as deleted and added; unchanged words inside it are included):

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B-1 | 265 | 112 | +153 |
| B-2 | 186 | 3 | +183 |
| Total | 451 | 115 | +336 |

B-2 breakdown: AC-1.1 +51 added / 3 deleted (the word "no" became "neither `/sc:load` nor any"); AC-1.2 +24; P1 row +24; load row +87.

## Disposition per finding

| Finding | Result | Where | What changed |
|---|---|---|---|
| B-1 (AC-0.4 requires a step Phase 0 cannot pass) | Applied | `SPEC:194` (AC-0.4 pass condition) | Step 3 is no longer required in full at P0: it needs exactly one `worker_done` whose `--outcome` matches the status in the command's existing report (the 3.1 "Report today" column, `SPEC:81-92`), with that file as the report path. Step 4 is `test -s` on that same file, not the YAML parse of `status` and `command` (`SPEC:183`). The text says the contract arrives in P1. Step 7.2 itself (`SPEC:182-183`) is unchanged, so P1 and later still use the full check. |
| B-2 (AC-1.1 and P1 require a contract for `/sc:load`) | Applied | `SPEC:195` (AC-1.1), `SPEC:196` (AC-1.2), `SPEC:159` (P1 row), `SPEC:112` (load row) | `/sc:load` is excluded from the section-presence assertion, the live check and the flag. The load row states once that it takes no `--unattended` and gets no `## Unattended mode` section or contract, which agrees with the row's own "none (see note)" (`SPEC:112`), the Decisions row (`SPEC:265`) and `INV-B:65`. AC-1.1 asserts load has no such section. The P1 usage-line fix for load (`SPEC:159`, SA-4 at `SPEC:149`) is kept. |

## Notes

- `SPEC:76` ("Every changed command also gains the `## Unattended mode` section") was not edited, because no blocking finding names it. The load row (`SPEC:112`) now states the exception, and AC-1.1 enforces it.
- Nothing was rejected. No rule, mechanism or section was added beyond the exceptions above; every addition carries its finding id.
- Not checkable in this sandbox, so UNVERIFIED: the real report file name and `status` values of the adversarial and workflow commands at P0 (`SPEC:83,92` say the filename is not fixed and the contract exists today; the status vocabulary is the open M-7 question). AC-0.4 therefore points at "the command's existing report" without naming a path for each.
