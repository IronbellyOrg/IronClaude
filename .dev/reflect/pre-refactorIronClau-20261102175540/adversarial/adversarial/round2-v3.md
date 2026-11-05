# Round 2 — Variant 3 Advocate rebuttal

## Response to criticisms
- R3-F2 covers check 1 only: conceded. CLAUDE.md:66 "If it shows the wrong owner, close it immediately and reopen" is an upstream PR action; R3-F2's AC would pass with it in place. C-001 goes to V1.
- R3-F2 relies on an unchecked `gh repo set-default --view`: partly rebutted. `gh repo set-default --help` confirms `-v, --view    View the current default repository`; whether it calls the network is still inferred. Sound but narrower than V1's fix.
- All six labelled drift; C-003, C-004 never assessed: conceded. R3-F1 is a spec gap (the plan copies source.md's grep exactly); R3-F4 a missing test.
- R3-F6 "weak": conceded on classification. Plan :82 lists link-forbidding only as "Orca `--issue`/`--pr` linking to the upstream repository", supporting the tool/flag reading of :73. Survives as a request to tighten wording ("narrow plan :73 to say 'link flags'").

## Updated assessment of other variants
- V1: strongest on correctness and C-001; its Round 2 move on X-001 to "2" abandons its original "ambiguous" reading, which plan :82 and blind calibration support.
- V2: right structure, wrong missing-requirements verdict; R2-F4 withdrawn; equal to V1 on C-004.

## New evidence
- `gh repo set-default --help` confirms `-v, --view`; network behaviour unverified.
- Plan :82's AC names only Orca `--issue`/`--pr` linking, so plan :73 most naturally means flag links; decides X-001 for "ambiguous".

## Final per-point positions
| Point | Superior | Reason |
|---|---|---|
| S-001 | 2 | Explicit missing-requirements audit |
| S-002 | 1 | Mixed labels fit the taxonomy |
| S-003 | 1 | Disputes F1-F4 with verified corrections |
| C-001 | 1 | Only card naming CLAUDE.md:64 and :66 |
| C-002 | 1 | "Narrow the wording" matches the calibrated reading of plan :73 and :82 |
| C-003 | 1 | Necessary class plus Blocked status |
| C-004 | tie (changed from 1) | Same three tests; both need `-rs` and zero skips |
| C-005 | 2 | Literal reading; V1 conceded |
| X-001 | 1 | Plan :82 limits "link" to Orca flags; "ambiguous" is right |
| X-002 | 3 | eval_runner.py:143 list arguments, never removed |
| A-001 | tie (changed from 3) | All advocates agree only routing_table.py:352 reads root CLAUDE.md |
| A-002 | tie | Holds on this host only |
| A-003 | 3 | skipif at test_git_replay_integration.py:56 |
