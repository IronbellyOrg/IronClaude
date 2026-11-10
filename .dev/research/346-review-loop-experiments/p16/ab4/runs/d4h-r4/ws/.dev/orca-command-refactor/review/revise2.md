# Revise 2: blocking findings M4 and N1

Candidate revised in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
Baseline for this revision (sha256 `7c8aa27b2871ce92c01502f179de64ec96be2031fdf14b1198dc4230f55a9adc`, 62793 bytes), taken from `review/round2.md` (`candidate:` line, `round2.md:10`).
Input review: `review/round2.md` (`review: 2 of 3`, `Reviser brief` at `round2.md:158-164`, `verdict: FAIL`).
VERIFY reply: `review/verify-2.md:12` (`confirmed: M4, N1`). Both ids were confirmed; none was rejected.
IDS: M4, N1 (`round2.md:160`).

## Byte accounting

Size before: 62793 bytes (sha256 `7c8aa27b2871ce92c01502f179de64ec96be2031fdf14b1198dc4230f55a9adc`).
Size after: 63106 bytes (sha256 `5c1ab8696d3015841916a6b721ba37673ca41cc95d7518dd2f44d176aa42898f`).
Net: +313 bytes = 1413 added - 1100 deleted.

| Edit | Spec location (after revision) | Finding | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|---|
| E1 | section 6, P0 row, column "Phase"/"Scope" and "Commands" cell (`specs/...spec.md:158`) | M4 | 213 | 217 | +4 |
| E2 | section 7.3, AC-0.4 row (`specs/...spec.md:206`) | M4 | 641 | 790 | +149 |
| E3 | section 7.3, AC-1.1 row (`specs/...spec.md:207`) | N1 | 246 | 406 | +160 |
| Total | | | 1100 | 1413 | +313 |

Per finding: M4 = 854 deleted, 1007 added (net +153). N1 = 246 deleted, 406 added (net +160). Byte counts were measured on the edited strings as UTF-8 (`wc -c`); the file total was measured with `wc -c` before and after.

## Dispositions

| id | Disposition | Where applied | Reason and citation |
|---|---|---|---|
| M4 | Applied, option 2 of the reviewer's recommendation (drop adversarial from the P0 smoke set and defer its contract check to P1). Option 1 (name a P0 file) was not taken because no fixed filename exists in the workspace to cite. | `specs/...spec.md:158` (P0 row: "two ready commands", the smoke list is `/sc:troubleshoot` and `/sc:workflow --handoff none`, adversarial marked as not a P0 smoke run, M4); `specs/...spec.md:206` (AC-0.4 lists two commands; new sentence states adversarial is not run in P0 because the spec names no fixed report file for it before P1, citing `inventory/commands-a.md:35,60`, and its direct-route check moves to AC-1.2 after AC-1.4 fixes the filename) | Candidate text that M4 quotes: `specs/...spec.md:206` "step 4 is `test -s` on that report" for adversarial, and `specs/...spec.md:195` "In P0 only `test -s` on the command's existing report applies". The candidate's own adversarial row says "filename not fixed" (`specs/...spec.md:83`). The inventory confirms that the skill names no filename (`inventory/commands-a.md:35`) and that earlier runs wrote the contract in two locations (`inventory/commands-a.md:60`). Both inventory lines were checked directly in the workspace; the verifier note that they were absent (`review/verify-2.md:9`) does not hold, because `inventory/commands-a.md` is present. AC-1.2 (`specs/...spec.md:208`) and AC-1.4 (`specs/...spec.md:210`) already cover adversarial after P1, and `specs/...spec.md:83` and `specs/...spec.md:158` put its contract fix in P1, so no check was lost. The section 1.4 evidence gap is still covered by the two remaining direct runs. |
| N1 | Applied, option 1 of the reviewer's recommendation (narrow the AC-1.1 section check to section 3.1 and the P1 rows of section 3.2). SPEC:79 and SPEC:159 already state the P1 scope and were not changed. | `specs/...spec.md:207` (AC-1.1) | Conflict cited in N1 (`round2.md:120-126`): P1 scope adds the flag to all of 3.1 and 3.2 (`specs/...spec.md:159`), adds the section only to the ten 3.1 commands (`specs/...spec.md:79`), but AC-1.1 required the section for every 3.1-3.2 command (`specs/...spec.md:207` before revision). auggie-review is phased P2 (`specs/...spec.md:100`), so the literal check fails for it in P1. The narrowed check now covers section 3.1 and the P1 rows of section 3.2 (analyze, build, business-panel, design, document, explain, index, test, and load, which stays excluded by M1). The P2-P4 section 3.2 commands are stated to get their section in their own phase, which matches `specs/...spec.md:76` ("Every changed command also gains the section"). |
| N2 | Not revised: not in IDS (`round2.md:160`). | none | Medium follow-up (`round2.md:128-130`); left alone per the REVISE prompt ("Leave minor and Medium findings alone"). |
| N3 | Not revised: not in IDS. | none | Medium follow-up (`round2.md:132-134`). |
| N4 | Not revised: not in IDS. | none | Medium follow-up (`round2.md:136-138`). |
| N5 | Not revised: not in IDS. | none | Medium follow-up (`round2.md:140-142`). |

## Checks on the edited text

- The P0 smoke set is now two commands in both `specs/...spec.md:158` and `specs/...spec.md:206`. No other mention of a three-command P0 set or an adversarial P0 smoke run remains (`grep -n 'three\|smoke'` on the spec returns only the unrelated "three approval gates" at line 105 and the "three scans" at line 172).
- AC-1.1 (`specs/...spec.md:207`) and the P1 scope (`specs/...spec.md:159`) and the section 3.1 phase note (`specs/...spec.md:79`) now agree: P1 adds the section to the ten 3.1 commands and to the P1 rows of 3.2.
- No new rule, mechanism or section was added beyond the parenthetical citations and the sentence that defers adversarial. Non-blocking findings N2-N5 and M3 were not touched.
- Repo scans and the pytest run are not applicable to this document-only revision and were not run. Inventory line citations used above were checked against `inventory/commands-a.md` in the workspace.
