# Spec panel fix log, cycle 1

SPEC: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`
REVIEW: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-review.md`
Date: 2026-11-08

## Decision applied

Owner decision 1 (coordinator `msg_9d0851e4c489`), applied through SP-01, SP-02 and SP-03:

- The Orca allowlist is seven verbs: `orchestration run-current`, `orchestration worker-list` (never `--include-remote`), `orchestration worker-show`, `orchestration task-list` (plain and `--ready`), `worktree ps` (never `--agent-wait`), `worktree list`, `worktree current`. That is eight templates, because `task-list` has two forms.
- Condition 1: an exact-set test pins the list, with negative tests for `--include-remote` and `--agent-wait` (new NFR-014).
- Condition 2: the lock claim is version-scoped, `unlikely (checked for Orca 1.4.245)`, falling back to `UNVERIFIED` on another version (new NFR-015). The version source is the `version` field of `/opt/Orca/resources/app.asar.unpacked/out/package.json`, marked an UNVERIFIED design choice; matching uses the leading MAJOR.MINOR.PATCH part.
- Section 13 rewritten; the section 8 table matches the seven verbs; rule 4(b), the gate policy line and worktree discovery are kept.

## Findings fixed

| ID | Severity | SPEC section | What changed | Status |
|---|---|---|---|---|
| SP-01 | CRITICAL | 8, 13, 4 (NFR-003, NFR-014), 15 (GQ-109) | Allowlist intro and table use the seven verbs and eight templates; both flags forbidden; section 13 rewritten; NFR-014 pins the exact set; NFR-003 negatives add both flags | FIXED |
| SP-02 | MAJOR | 8 (disk reads), 9, 11, 12 (R3), 13, 4 (NFR-015) | Version file is a disk read; header line and bullet are version-scoped with `CHECKED_ORCA_VERSION`; "always printed" removed; index.lock row and R3 updated | FIXED |
| SP-03 | MAJOR | Frontmatter, status row, 13, 17.1 | Gate text records sign-off with two conditions; checklist covers NFR-001 to NFR-015 and both conditions; release precondition is NFR-014 and NFR-015 passing | FIXED |
| SP-04 | CRITICAL | 4 (NFR-009) | AC replaced with the subset-and-type golden test from the review (adds `worktrees[]` per SP-05) | FIXED |
| SP-05 | CRITICAL | 3 (FR-005), 5.2, 9 | FR-005 AC is 4 `rows`, 2 `worktrees`, `(4/4)`; reconciliation formula; JSON gains `worktrees` and summary keys `visible`, `historical`, `total`, `total_is_lower_bound` | FIXED |
| SP-06 | MAJOR | 7 (SweepInput), 4 (NFR-005), 5.3 | `collected_start` and `collected_end` added; byte identity apart from `report_path`; suffixes `-2` to `-99` with exclusive create, then exit 1 | FIXED |
| SP-07 | MAJOR | 7 (rule 6, package states), 8, 3 (FR-026) | `guard refused:` first-line anchor; `FINAL:` line anchor with negative fixture; `runtime_unavailable` only as error field or whole first stderr line, with negative AC; FR-026 test (1) updated | FIXED |
| SP-08 | MAJOR | 8, 3 (FR-020), 9, 11 | Budget-cut timeout is `call_failed` with `unscanned: time budget reached (90 s)`; no call under 1 s; cap reason `unscanned: show cap reached (50)`; old reason string replaced everywhere | FIXED |
| SP-09 | MAJOR | 3 (FR-002, FR-018), 5.1, 8 | `--run` regex check before any `_orca` call, exit 2 message, duplicates collapsed, unknown-Run shape is `call_failed`; four AC examples | FIXED |
| SP-10 | MAJOR | 8, 3 (FR-020), 4 (NFR-007), 9 | Git 10 s timeout counts against 90 s; cap split across Runs; `bound_reached` defined and cap line only when at least 1; NFR-007 120 s AC; exact-50 and two-Run ACs | FIXED |
| SP-11 | MAJOR | 3 (FR-004) | `--output` must be `<root>/.dev/sweeps/` or below; four AC cases | FIXED |
| SP-12 | MAJOR | 3 (FR-022) | Fallback is `uv run --frozen --no-sync superclaude sweep run`; test asserts `--no-sync`; flag effect to confirm at design | FIXED |
| SP-13 | MAJOR | 7 (rule 1) | Rule 1 declines with `gate_policy` None; with Orca None matches only on a Ruling halt, else note; two rule-table tests | FIXED |
| SP-14 | MAJOR | 7 (rules 4(b), 8, 9), 9, 3 (FR-006, FR-009), 4 (NFR-010) | New rule 8 `person_active`; fallback is rule 9; ready Tasks under their own sub-heading with a count; cross-references renumbered | FIXED |
| SP-15 | MAJOR | 7, 3 (FR-007, FR-011) | `last_activity` source and Waiting (a) age defined; FR-007 AC and FR-011 point to them | FIXED |
| SP-16 | MAJOR | 7 (SessionRow), 9, 3 (FR-010) | `row_id`, its format and the join key; empty or stale tab map gives a coverage reason and None, not True | FIXED |
| SP-17 | MAJOR | 8, 3 (FR-015), 9, 14 (INV-008), 15 (GQ-110) | Git argv `--porcelain=v1 -z --branch --untracked-files=all`; parsing bullets and fixtures; untracked-path consequences updated, override of `status.showUntrackedFiles` kept UNVERIFIED | FIXED |
| SP-18 | MAJOR | 3 (FR-003, FR-004), 7 | `--window` regex, ASCII, max `720h`/`30d`; `window_start = now - window`; `--root` validation messages and ACs | FIXED |
| SP-28 | MAJOR | 8, 3 (FR-020) | Popen with 8 MiB kill; transcript tail is the normal case; hit is greater than 1 MiB; contract hit unscanned, ledger read as head and tail; limit minus 1, at, plus 1 fixtures | FIXED |
| SP-29 | MAJOR | 3 (FR-010) | Any-Run worker transcript is never True; out-of-scope Run gives False with note; R1/R2 fixture; tab map fields UNVERIFIED | FIXED |

Counts: FIXED 20, ESCALATED 0, PARTIAL 0.

## MINOR touched

- SP-25: covered by SP-12 (both `allowed-tools` literals now named in FR-022) and SP-08 (two separate reasons for the two bounds in FR-020 and section 11).
- No other MINOR finding (SP-19 to SP-24, SP-26, SP-27) was edited.

## Escalated to owner

None. No G-n entry was added to section 18. G-1 stays open: SP-20 (where `write_report` lives) ties to G-1 and was not done in this cycle, so G-1 is unchanged.

## Post-fix checks

Greps over the SPEC after all edits:

| Pattern | Result |
|---|---|
| `five read verbs`, `five verbs`, `five` | 0 hits |
| `needing owner sign-off`, `release gated`, `signs off on INV-005`, `not released` | 0 hits |
| `6 rows` | 0 hits |
| `always printed` | 0 hits |
| `no requirement in this spec depends` | 0 hits |
| `call bound reached` | 0 hits |
| `git effects on worker worktrees` | 0 hits |
| `status --porcelain --branch` | 0 hits |
| `untracked-files=normal` | 0 hits |
| `Orca read verbs UNVERIFIED`, `NFR-001 to NFR-013` | 0 hits |
| `rule 8` | 1 hit, line 261, the new numbering line (rule 8 is now `person_active`); intended |
| `showUntrackedFiles` | 3 hits (FR-015, section 9 bullet, INV-008), all new text stating the flag override as UNVERIFIED; intended |
| Em dash | 0 hits |
| Duplicate FR or NFR IDs | none; FR-001 to FR-026 unchanged, NFR-014 and NFR-015 added after NFR-013 |
| `[SP-` tags | present for all 20 findings in scope |

SPEC line count: 653.

## Self-audit

- Only SPEC and this LOG were edited; REVIEW and EVIDENCE were read only.
- Every SPEC edit was preceded by a Read of that text.
- No FR or NFR was renumbered. Rule rows were renumbered (fallback 8 to 9) because SP-14 asks for a new rule; every cross-reference was updated (FR-006, FR-009, NFR-010, section 7 numbering line).
- Dependent text fixed in the same pass: removing the `showUntrackedFiles` limitation (SP-17) required edits to FR-015, the section 9 header, INV-008 and GQ-110; the reason-string change (SP-08) required edits to FR-020, section 9 and section 11; the JSON shape change (SP-05) required edits to 5.2, section 9 and NFR-009.
- Scope: no addition beyond what a finding or owner decision 1 asked. The extra AC sentences (exact-50, two-Run, stderr later-line marker, record timestamp in FR-007) restate the review's recommendations as testable cases.
- UNVERIFIED items kept marked: the Orca version source and matching rule, the unknown-Run stderr shape, the tab map Run id field, the `uv run --frozen --no-sync` effect, and the git override of `status.showUntrackedFiles`.
- Not checked: whether the review's line numbers still match after the merge (fixes were placed by content, not by the review's line numbers).
