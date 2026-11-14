# Spec panel fix review, cycle 1

SPEC: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (653 lines)
REVIEW: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-review.md`
FIXLOG: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-fix-log-1.md`
EVIDENCE: `.dev/issues/339/analysis/inv-005-orca-index-lock.md`
Owner decision: coordinator `msg_9d0851e4c489` (seven verbs, two conditions)
Date: 2026-11-08

## Verdict

**PASS.** All 20 in-scope findings (SP-01 to SP-18, SP-28, SP-29) are fixed in the SPEC, and the fixes match the owner decision. I found 0 blocking findings and 10 minor notes. None of the minor notes changes runtime behaviour or makes two requirements contradict each other in a way an implementer could not resolve.

## Per-finding check

| ID | Fixed? | Evidence (SPEC section, quoted words) | New issue |
|---|---|---|---|
| SP-01 | yes | Section 8 line 301: "The templates use exactly the seven verbs of INV-005 condition 1 (section 13) and no other verb; `task-list` has two forms, so there are eight templates." Table lines 305-312 list those eight. Line 323 forbids both flags and "changes only the forms of the seven verbs, never the verb set". Section 13 lines 495-504 list the seven. NFR-014 line 143 pins them. | Minor M1 (section 2 line 83 says `--include-remote` is out "until its cost is measured", not "never"); minor M2 (`run-current` template has no `--json`); minor M3 (`worktree list` and `worktree current` are listed but have no consumer yet) |
| SP-02 | yes | Section 9 line 360: "Orca lock risk: <unlikely (checked for Orca 1.4.245) \| UNVERIFIED (checked for Orca 1.4.245; observed <version or unknown>)>"; line 367: "The lock line is printed on every run and is version-scoped". Section 8 line 340 makes the version file a disk read. Section 11 line 441: "unlikely for Orca 1.4.245 and UNVERIFIED on any other version". NFR-015 line 144. | none |
| SP-03 | yes | Frontmatter line 9: "INV-005 owner sign-off recorded 2026-11-08 with 2 conditions". Line 26 status: "signed off 2026-11-08 with two conditions (section 13), which are release preconditions". Section 13 line 483 records the sign-off; lines 511-513 record both live probes and their limits. Section 17.1 lines 618-620 cover NFR-001 to NFR-015 and both conditions; line 627 release precondition. | Minor M4 (the limits line does not say `worker-show` was never live-probed) |
| SP-04 | yes | NFR-009 line 138: subset-and-type golden test, including `worktrees[]`. | none |
| SP-05 | yes | FR-005 line 99: "4 entries in JSON `rows` and 2 entries in JSON `worktrees`; ... `(4/4)`". Section 5.2 lines 163-169 add `worktrees` and summary keys `visible`, `historical`, `total`, `total_is_lower_bound`. Section 9 line 392 JSON shape matches. | Minor M9 (fixture does not say the person session is active, which rule 8 now needs) |
| SP-06 | yes | Section 7 line 230: `collected_start` and `collected_end`. NFR-005 line 134: byte identity apart from `report_path`. Section 5.3 line 174: suffixes `-2` to `-99`, exclusive create, then exit 1 `report name space exhausted`. | none |
| SP-07 | yes | Rule 6 (section 7) uses a first-line `guard refused:` anchor; line 259: "a body whose later line quotes `guard refused:` is not finished." Line 269: `FINAL:` line anchor with a negative fixture. Section 8 line 287: `runtime_unavailable` only as the error field or the whole first stderr line, with a negative AC. FR-026 line 120 test (1) updated. | none |
| SP-08 | yes | Section 8 lines 290-292: a budget-cut timeout is `call_failed` with `unscanned: time budget reached (90 s)`; no call starts with under 1 s left (AC: 88.5 s then 1.5 s timeout; 89.5 s means no call); cap reason `unscanned: show cap reached (50)`. FR-020 line 114 and section 11 line 445 use the same strings. Grep `call bound reached` gives 0 hits. | none |
| SP-09 | yes | FR-002 line 96: `--run` regex check "before any `_orca` call", exit 2 message, duplicates collapsed, unknown-Run shape is `call_failed`, four AC examples. Section 5.1 line 158: "an empty or invalid `--run` value, FR-002 [SP-09]". | Minor M5 (FR-019 line 113 still repeats the old FR-002 paragraph without the SP-09 text) |
| SP-10 | yes | Section 8: git 10 s timeout counts against 90 s; cap split across Runs. Section 9 line 370: `bound_reached` defined; cap line only when at least 1. NFR-007 line 136: 120 s AC. FR-020 line 114: exact-50 and two-Run ACs. | none |
| SP-11 | yes | FR-004 line 98: `--output` must be `<root>/.dev/sweeps/` or below, four AC cases. | none |
| SP-12 | yes | FR-022 line 116: `uv run --frozen --no-sync superclaude sweep run`; test asserts `--no-sync`; flag effect marked to confirm at design. | none |
| SP-13 | yes | Rule 1 (section 7 line 249): declines when `gate_policy` is None; with Orca None it matches only on a Ruling halt, else adds a note; two rule-table tests. | Minor M6 ("adds that note" could be read as pointing to the wrong note) |
| SP-14 | yes | Rule table lines 249-257: rule 8 `person_active`, rule 9 fallback. Line 261: "places it as rule 7, the active person session as rule 8 [SP-14] and the fallback as rule 9". Section 9 line 378: ready Tasks under their own sub-heading with `Ready Tasks: <N>`. FR-006 line 100, FR-009 line 103, NFR-010 line 139 renumbered. | Minor M10 (FR-006 wording "rules 1-7 plus idle") |
| SP-15 | yes | Section 7 lines 237-238 define the `last_activity` source and the Waiting (a) age. FR-007 line 101 and FR-011 line 105 point to them. | none |
| SP-16 | yes | Section 7 line 235: `SessionRow.row_id` and its format; line 236 join rule. FR-010 line 104: empty or stale tab map gives a coverage reason and None, not True. Section 9 JSON carries `row_id`. | none |
| SP-17 | yes | Section 8 git template: `--porcelain=v1 -z --branch --untracked-files=all`, with parsing bullets and fixtures (lines 325-336). FR-015 line 109, section 9 line 361, INV-008 line 526, GQ-110 line 563 all use the new argv; the `status.showUntrackedFiles` override is marked UNVERIFIED. | Minor M7 (line 335 "gives unpushed N" against the `bool \| None` type of `WorktreeState.unpushed` at line 240; the no-upstream branch line is not in the parsing list) |
| SP-18 | yes | FR-003 line 97: `--window` regex, ASCII only, max `720h` / `30d`. Section 7 line 229: `window_start = now - window`. FR-004 line 98: `--root` validation messages and ACs. | none |
| SP-28 | yes | Section 8 line 286: Popen with an 8 MiB kill; lines 293-297: transcript tail is the normal case, a hit is greater than 1 MiB, a contract hit is unscanned, the ledger is read as head and tail; limit minus 1, at and plus 1 fixtures. FR-020 line 114. | Minor M8 (the "first 512 KiB and last 512 KiB (split proposed)" split goes beyond the review's text) |
| SP-29 | yes | FR-010 line 104: an any-Run worker transcript is never True; an out-of-scope Run gives False with a note; R1/R2 fixture; tab map fields UNVERIFIED. | none |

## Allowlist consistency

The owner's seven verbs appear identically in every place that names them:

| Place | What it says | Consistent? |
|---|---|---|
| Section 8 intro (line 301) | seven verbs, eight templates, no other verb | yes |
| Section 8 table (lines 305-312) | `run-current`; `worker-list --run <run> --json` "Never with `--include-remote`"; `worker-show`; `task-list --run` and `task-list --ready --run`; `worktree ps --json` "Never with `--agent-wait`"; `worktree list --json`; `worktree current --json` | yes |
| Section 8 line 323 | both flags forbidden; never the verb set | yes |
| Section 13 (lines 495-504) | the same seven, both flag bans, exact-set test with negatives (NFR-014) | yes |
| NFR-003 (line 132) | negatives include `worker-list --include-remote` and `worktree ps --agent-wait`; points to NFR-014 for the exact set | yes |
| NFR-014 (line 143) | the same seven verbs and eight templates | yes |
| Rule 4(b) (section 7) and section 8 line 308 | `task-list --ready` feeds rule 4(b) | yes, a listed verb |
| Gate policy line | read from the Task spec through `task-list`, a listed verb | yes |
| Worktree discovery (line 310) | `worktree ps --json` | yes, a listed verb |
| GQ-109 (line 562), 17.1 (line 619), release precondition (line 627) | seven-verb set pinned, both flags forbidden | yes |

Unlisted verbs: a grep for `orchestration [a-z-]+`, `worker-read`, `gate-list` and `run-list` finds every hit outside the seven only in exclusion text (section 2 line 83, FR-002 line 96, FR-021 line 115, NFR-003 line 132, section 8 line 323, section 11 line 447, GQ-104 line 557, GQ-109 line 562). No requirement calls an unlisted verb.

Listed but unused: `worktree list` and `worktree current` have no consumer; lines 311-312 defer the choice to /sc:design. That is allowed by the owner decision (minor M3).

## Rule numbering

- The table has 9 rules: 1 `blocked_contract`, 2 `orca_exit_proof`, 3 `fenced`, 4 `waiting_signal` (with 4(b)), 5 `working`, 6 `finished`, 7 `idle`, 8 `person_active`, 9 `fallback`.
- Line 261 states the order: idle rule 7, active person session rule 8, fallback rule 9.
- FR-006 line 100, FR-009 line 103 ("rule 9 (the fallback)") and NFR-010 line 139 ("9 rules, ending `person_active`, `fallback`") match.
- Line 259 "AC for rule 6" still points to `finished`, which is still rule 6.
- GQ-103 and GQ-105 (section 15 lines 552-558) name no rule number, so nothing there needed renumbering.
- Section 15 and the Change references cite changes and source lines, not rule numbers.
- A grep for `rule [0-9]` found no stale reference to the old fallback number 8.

## New NFRs

| NFR | AC present? | Traces to |
|---|---|---|
| NFR-014 (line 143) | yes: exact-set test that `ALLOWED_ORCA` equals the pinned eight templates; negatives for `--include-remote` on `worker-list`, `--agent-wait` on `worktree ps`, and any other verb, each raising `ValueError` before a subprocess starts | SP-01 and INV-005 condition 1; checklist line 619; release precondition line 627 |
| NFR-015 (line 144) | yes: `1.4.245-aidev02.780594c521aa` gives `unlikely`; `1.4.246` gives `UNVERIFIED` naming it; a missing or unreadable file gives `UNVERIFIED` naming `unknown` | SP-02 and INV-005 condition 2; checklist line 620; release precondition line 627 |

The version source and the MAJOR.MINOR.PATCH matching rule are marked UNVERIFIED design choices in NFR-015 and in section 13 condition 2 (line 505). The observed value on the checked host matches EVIDENCE line 9.

## Contradiction scan

| Grep | Result |
|---|---|
| `6 rows` | 0 hits |
| `five` | 0 hits |
| `BLOCKED_BY_INVARIANTS` | 1 hit, line 10, past tense: "was BLOCKED_BY_INVARIANTS on INV-005; resolved by static and live evidence". No contradiction. |
| `sign-off not recorded` | 0 hits |
| `needing owner sign-off` | 0 hits |
| `exit 0` | 1 hit, FR-001 line 95, about `--help` under `CliRunner`. Unrelated to the fixes. |
| `UNVERIFIED` | Lock-line hits (lines 144, 360, 367, 441, 505) all say UNVERIFIED only for a different or unknown Orca version, matching the owner condition. Other hits mark design choices (version source, matching rule, `--no-sync` effect, tab map fields, untracked override, run id shape). None claims a fact the sign-off settled. |
| `rule 8` | 1 hit, line 261, the new numbering line. Correct. |
| `rule 9` | FR-009 line 103 and line 261. Correct. |
| `include-remote` | lines 83, 132, 143, 306, 323, 497, 504, 562, 619. All forbid it in Phase 1; line 83 phrases it as "until its cost is measured" (minor M1). |
| `agent-wait` | lines 132, 143, 310, 323, 500, 504, 510, 562, 619. All forbid it. |
| `call bound reached` | 0 hits |
| Em dash | 0 hits |

## Blocking findings

None.

## Minor notes

- **M1.** Section 2 line 83 lists `--include-remote` as out of Phase 1 "until its cost is measured (GQ-22)", while sections 8 and 13 say "never". It does not change Phase 1 behaviour, but a reader could think it can be added inside Phase 1. Suggest: "`--include-remote` (forbidden by INV-005 condition 1; GQ-22 for a later phase)".
- **M2.** The `orchestration run-current` template (line 305) has no `--json`, unlike the other Orca templates and the review's recommendation. Confirm at the step 1.0a capture whether the parser needs it.
- **M3.** `worktree list` and `worktree current` are in the allowlist with no consumer (lines 311-312). The owner allowed them; decide at /sc:design or drop them from the pin together with an owner note.
- **M4.** Section 13 line 513 lists the probe limits but does not say that `orchestration worker-show` was never live-probed (probe 1 used four verbs, probe 2 three). The claim for it rests on the static read alone. Suggest adding: "`worker-show` was checked statically only."
- **M5.** FR-019 line 113 repeats the pre-fix FR-002 paragraph and lacks the SP-09 `--run` check. Not in scope (SP-19), but the two texts now differ.
- **M6.** Rule 1 (line 249): "adds that note" can be read as the ask-the-coordinator note rather than the Ruling-halt note. Name the note.
- **M7.** Section 8 line 335 says the branch line "gives unpushed N", but `WorktreeState.unpushed` at line 240 is `bool | None`. Also, the no-upstream branch line is not in the parsing list; state that it gives None.
- **M8.** The ledger "first 512 KiB and its last 512 KiB (split proposed)" (section 8, lines 293-297) is a scope addition beyond the review text. It is marked proposed and does not change any other requirement.
- **M9.** The FR-005 fixture (line 99) does not say the person session is active, so rule 8 versus Historical placement is not pinned by that fixture.
- **M10.** FR-006 line 100 "(REPORT rules 1-7 plus idle and person session (active))" mixes REPORT numbering with spec numbering. Suggest "spec rules 1-9 (section 7)".

## Self-audit

- I found zero blocking issues, so I tried to break the PASS in four ways: (1) grepped for every Orca verb form to find an unlisted verb in a requirement (none outside exclusion text); (2) grepped `rule [0-9]` for a stale fallback number (none); (3) checked that every `UNVERIFIED` lock-line hit is version-conditional, not a leftover blanket claim (all are); (4) checked that both new NFRs are in the checklist and the release precondition (they are, lines 619, 620, 627).
- I checked the section 13 evidence against EVIDENCE: the version string at EVIDENCE line 9, the task-list and `worktree ps` addendum (EVIDENCE lines 150-158) and the `--agent-wait` reason all match section 13 lines 505-510.
- Limits of this review: I read the SPEC in chunks and through greps, not every line in one pass. I did not re-run the FIXLOG greps for `always printed`, `status --porcelain --branch` or `untracked-files=normal`. I did not check that the REVIEW's line numbers match the merged SPEC. I did not edit the SPEC or any other file; only this review file was written.
