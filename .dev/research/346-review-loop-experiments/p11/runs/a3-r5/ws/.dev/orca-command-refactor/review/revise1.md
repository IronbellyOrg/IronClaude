# Revise 1: Orca worker-contract spec

- Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51`. Values: candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, IDS = F-1, F-2, F-3 (the ids listed at `.dev/orca-command-refactor/review/round1.md:193`).
- Inputs read: `.dev/orca-command-refactor/README.md` (binding context), `review/round1.md` (all), the spec (all), `inventory/commands-a.md:35,60-61` and `inventory/commands-b.md:240-245,267-275` (the lines the F-2 edit cites; checked, each matches the claimed row). Other inventory lines were not re-read; citations the edits reuse are the ones the spec already carried.
- Not run: the spec-panel. No PASS is claimed. Medium findings M-1 to M-16 and the minor notes were left alone.
- Line numbers: no line was added or removed, so every `S:N` citation in `round1.md` still points at the same line. All edits are in-line replacements (8 lines changed: 73, 76, 159, 176, 193, 194, 195, 196).

## Byte accounting

Method: byte counts from `wc -c`; per-line added/deleted bytes from a character-level diff of `.dev/orca-command-refactor/specs/history/spec-v1.md` (byte-identical to the file reviewed in round 1, same sha256) against the revised spec, summed per edited line, UTF-8 bytes.

| | bytes | sha256 |
|---|---|---|
| Before (reviewed in round 1) | 57763 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| After | 58448 | `5d3d225a6ef33d0f0c3eb9b745dd4e780b4ca5a0b2dd745dd00ce966449d2b61` |
| Net | +685 | |

| Finding | Lines edited | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| F-1 | 73, 76, 159, 195, 196 | 293 (42 + 106 + 95 + 32 + 18) | 31 (0 + 4 + 20 + 7 + 0) | +262 |
| F-2 | 194 | 345 | 9 | +336 |
| F-3 | 176, 193 | 91 (66 + 25) | 4 (2 + 2) | +87 |
| Total | 8 lines | 729 | 44 | +685 |

Check: 57763 + 729 - 44 = 58448.

## One row per finding id

| Id | Disposition | Where applied | What changed and why |
|---|---|---|---|
| F-1 | Applied (narrowed scope; nothing new added beyond one phrase per edit, each citing F-1) | Spec line 159 (section 6, P1 scope); line 195 (AC-1.1); line 76 (section 3 intro); line 73 (section 2.3); line 196 (AC-1.2) | Line 159: "accepted by every command in sections 3.1 and 3.2" became "accepted by the commands in the next column only", with the rule that a command first accepts the flag in the phase that converts its gates. This is the narrowing round1 recommends (`round1.md:44`) and removes the 37-versus-13 divergence (`round1.md:43,165-173`): the flag now reaches only the 13 commands P1 names, so auggie-review (P2), implement, post-release and pr-submit (P4) cannot accept a no-op flag while their defaults stay on (WC-9, WC-2). Line 195: AC-1.1's quantifier is now "every command in the P1 row of section 6 except load", so load (no contract, `INV-B:57-65` via spec line 112) and pr-submit (P4, and absent from the P1 row, so D3(a) no longer contradicts the check) are out of the universal set; the clause "no section-4 command has one" is kept. Line 76: the sentence "Every changed command also gains the `## Unattended mode` section" would still force load and early sections onto commands, so it now says the section arrives in the command's own Phase and excludes load (consistency with line 159/195, same defect). Line 73: the brief template said every brief carries `--unattended`; it now says "once the command's phase has landed", otherwise a coordinator would pass a flag a P2-P4 command does not yet accept (the wrong outcome in `round1.md:42`). Line 196: AC-1.2's "each P1 command" also included load, which has no contract to check (same defect as AC-1.1), so it excludes load. |
| F-2 | Applied | Spec line 194 (AC-0.4) | Steps 1, 2 and 5-7 pass as written. Steps 3 and 4 now use the command's existing report file for P0, with the three files named: troubleshoot `REPORT.md`, workflow `.dev/tasks/to-do/<id>/return-contract.yaml`, adversarial its existing contract with the filename unfixed until P1 (`inventory/commands-b.md:242` and `:272`; `inventory/commands-a.md:60`). Step 3 compares `--outcome` with that file's own verdict and sets `--report-path` to it; step 4 is `test -s` only, because the `status`/`command` assertion of 7.2 step 4 needs the WC-4 fields that no P0 edit adds (`round1.md:55-56`). The 7.2 text itself is unchanged, so the WC-4 path check still applies to P1-P4. Rest of AC-0.4 (live check, record, "reopens section 1") unchanged. |
| F-3 | Applied | Spec line 176 (AC-C5); line 193 (AC-0.3) | `grep -E '^-[^-]'` replaced by `grep -E '^-' \| grep -v '^--- a/'` in both rows. I ran the new pipeline on a synthetic diff holding the file header `--- a/x.md`, a deleted bullet `-- Will Not: modify specs`, a deleted prose line and a deleted rule `----`: it prints the bullet, the prose line and the rule and drops only the header (terminal output in this run). AC-0.3 got the same pattern for consistency, since round1 names it in the finding title (`round1.md:59`) though it calls it safe in practice (`round1.md:63`). I did not add a "which removals the defect fixes allow" clause (`round1.md:64`): AC-C5's scope sentence already limits the check to command files edited without a named defect fix (SA-4), so on those files every removed line is a failure and a clause would add text for no case. |

## Not changed (listed so the next reviewer does not look for them)

- M-1 to M-16, the G-3 and G-8 GAP rows and the minor notes: out of scope for this revision. M-12 (a flag added to an existing Usage line is a `-` line, which AC-C5 now flags just as before) is unchanged in behaviour by the F-3 edit.
- Section 6's sentence "Phases 1-3 need no user decision" (M-8) and section 9 are untouched.
- Commands in 3.1 with "None" in the small-fix column (brainstorm, init-lite) now never gain the flag or section, because only commands in a phase row do. That follows from F-1's rule and from section 3.1's own wording that they run as workers today with the stated flags (spec line 79). Whether they should gain a no-op flag later is a design choice for the reviewer or user, not something a blocking finding calls for.
- Citations to files outside the workspace in the edited lines: none added. The new citations (`INV-B:242,272`, `INV-A:60`) point at files in the workspace and were read.

No PASS is claimed; the candidate is returned once for re-review.
