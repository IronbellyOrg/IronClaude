# Revise 1: orca-worker-contract-spec.md

Input: `review/round1.md` (Reviser brief, `round1.md:204-210`, blocking id B-1 only). Edited in place: `specs/orca-worker-contract-spec.md`. Nothing else was changed. The spec-panel was not run. No PASS is claimed. Citations are `SPEC:N` (line in the revised spec; line numbers did not move) and `R1:N` (`review/round1.md`).

## Byte accounting

| Measure | Bytes |
|---|---|
| Spec before (`wc -c`) | 57763 |
| Spec after (`wc -c`) | 57927 |
| Net | +164 |

| Finding id | Bytes added | Bytes deleted | Where |
|---|---|---|---|
| B-1 | 175 | 11 | `SPEC:112` (+117, -11), `SPEC:159` (+18), `SPEC:195` (+20), `SPEC:196` (+20) |
| All other ids | 0 | 0 | not touched |

Check: 175 - 11 = 164 = 57927 - 57763.

## Approach

B-1 (`R1:87-93`) says AC-1.1 and AC-1.2 demand a section and a contract for `load`, while the `load` row says it has none (`SPEC:112`) and the decision says a report file would be an unrequested addition (`SPEC:265`). R1's recommendation gives two options (`R1:92`): exclude `load` from the checks, or give `load` a one-line section. I took the exclusion: it adds a few words to four places, adds no file or section, and keeps the existing `load` decision. The other option would have added a section and a rule the decision rejects.

## Dispositions

| Finding id | Location named | Disposition |
|---|---|---|
| B-1 | `SPEC:112` (`load` row) | Applied. The Report cell "none (see note)" became "none" (the note pointed at nothing). The last column now says `load` gets no `## Unattended mode` section, no `--unattended` flag and no contract, so AC-1.1 and AC-1.2 skip it (B-1). The existing text (use it inside another worker's brief; usage-line fix) is kept. |
| B-1 | `SPEC:159` (P1 scope) | Applied. "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" now reads "... except load (B-1)", so P1 no longer promises the flag on `load`. The command list still shows "load (usage line only)". |
| B-1 | `SPEC:195` (AC-1.1) | Applied. The test asserts the section for every command in 3.1-3.2 "except `load` (B-1)". The section-4 negative assertion is unchanged. |
| B-1 | `SPEC:196` (AC-1.2) | Applied. The live check runs on each P1 command "except `load` (B-1)". This removes the `test -s <contract>` step 4 (`SPEC:183`) from `load`. |
| B-1 | `SPEC:265` (`load` decision) | No change needed. It already says no report file and "Only its usage-line defect is fixed", which agrees with the exclusion. |
| F-1 to F-9, N-1 to N-9 | n/a | Not touched, per the Reviser brief (`R1:208`) and the revise brief (minor and Medium findings left alone). |

## Residual risk (not edited, outside the named locations)

- `SPEC:76` ("Every changed command also gains the `## Unattended mode` section") and `SPEC:52` ("Each changed command adds a short `## Unattended mode` section") are general statements that `load`, a changed command through its usage-line fix, falls under read literally. The `load` row (`SPEC:112`) is the specific exception, and AC-1.1 and AC-1.2, which R1 treats as the mechanical tests, now agree with it. These two lines were not in the Reviser brief's list (`R1:207`), so I left them. A reviewer who reads them as binding could raise this again; the fix would be "except load" on each.
- The quantity flow in `R1:70-79` (37 expected, 36 produced) is resolved by the exclusion: AC-1.1 now expects 36 sections, and `load` is the 37th worker-capable command without one. This was checked by reading the edited lines, not by re-running the panel.
