# Spec refactor log: GitHub issue watcher (issue #331)

- Date: 2026-11-07
- Input: `merged-requirements.md` (left unchanged), `spec-panel-review.md` (PF-001..PF-048), `seed-brief.md`
- Output: `spec-final.md`
- Fixed owner decisions: D1 option A, D2 claim-only, D3 only a validated integer reaches a session prompt. No finding contradicted D1, D2 or D3, so none was rejected on that ground.

## Decisions per finding

Severity: C = CRITICAL, M = MAJOR, m = MINOR. "Where" names the spec-final.md requirement id or section.

| Finding id | Severity | Decision | Where in spec-final.md | One-line reason |
|---|---|---|---|---|
| PF-001 | C | APPLIED | Section 3 Intended owner; OD-3 | Verified: `refs/claim.md:41-42` accepts an unassigned issue, so "same rule as the claim" was false; the watcher rule is a strict subset. |
| PF-002 | C | APPLIED | FR-014 GWT | The GWT now separates a pre-pending `failed` (`launches` 0) from every post-pending case (`launches` 1). |
| PF-003 | C | APPLIED | FR-001 | Single cycle order; extended with the `enabled` check (PF-013), the cycle-start sweep (PF-042) and the final store write (PF-018) so the orders agree. |
| PF-004 | C | MERGED-INTO PF-036 | Section 3 Eligible issue | Panel conflict note: PF-004's state rule replaces the "no entry with `launches > 0`" clause inside PF-036's ordering. |
| PF-005 | M | APPLIED | Section 3 Own login; FR-002 | A login that fails the format check exits 3 `login_invalid` before discovery. |
| PF-006 | M | APPLIED | Section 3 Complete event history | 5-page cap per read [PROPOSAL] counted in the NFR-009 cap; opposing tie defined; skips `events_incomplete`. |
| PF-007 | M | APPLIED | Section 8 Reason codes; FR-020; FR-022 | Closed reason table added; `events_unreadable` split from `events_incomplete`. |
| PF-008 | C | APPLIED | Section 8 Acceptance | Count mismatch fixed: at most one launch per cycle, min(N, 6) per 24 h, the rest skip `day_cap`; the seed's N-mocked-issues sentence kept. |
| PF-009 | C | APPLIED | FR-016 GWT | Count mismatch fixed with k = min(10, floor((35 − 3)/r)). |
| PF-010 | M | APPLIED | Section 7 Schema; FR-005; FR-020 | `approved_at` added to the entry schema and decision lines. |
| PF-011 | M | APPLIED | NFR-013 (b), (d) | SLO excludes DISABLED and dry-run cycles; (d) covers `abandoned` `pending_orphan`. |
| PF-012 | m | APPLIED | R3 | Trivial: "100 or more" used throughout. |
| PF-013 | M | APPLIED | FR-027; FR-021; runbook step 9 | `enabled: false` exits 0 `not_enabled` with no health refresh; dry-run ignores `enabled`. |
| PF-014 | M | APPLIED | Section 3 Claimed; Section 7 transitions | Marker window defined; new `failed` → `claimed` row with `launches` 0. |
| PF-015 | M | APPLIED | FR-020 | Three stderr-only exceptions named; GWT gains the exit-2 case. |
| PF-016 | m | NOTED | FR-014 | Not trivial (changes retry semantics); a prompt `ValueError` is still retried as `failed`. Left for review. |
| PF-017 | C | APPLIED | FR-013; NFR-014; Section 8 Modules; Section 12 | Verified `_ORCA_CLIS` at `install_user_setup.py:35` and `_find_orca` at `:198-221`; `launch.find_orca(runner)` mirrors it with a parity test. |
| PF-018 | M | APPLIED | FR-023; FR-028 | `considered` stamps written in the final store write; entries written earlier in a rate-limited cycle stand. |
| PF-019 | m | NOTED | NFR-014 | Not trivial; the launcher Protocol is kept as the test seam. |
| PF-020 | m | APPLIED | NFR-002; Section 12 | Trivial: argv written as `gh api --method GET <path>`; verified `poll-augment-review.sh` `fetch_rest` (lines 46-77) is cited for paging only. |
| PF-021 | C | APPLIED | Section 8 Failure modes; exit table row 7; FR-022 | Exit 7 now covers pre-pending `failed`, `unknown` and `abandoned` `spawn_error`; non-transient re-read failure is `revalidation_failed`. |
| PF-022 | M | APPLIED | FR-028; FR-026 | Clamp to 3600 s [PROPOSAL] with `rate_limit_clamped`; `reset --rate-limit` verb added. |
| PF-023 | M | APPLIED | FR-020 | Rotation only under the lock; one `O_APPEND` write per line. |
| PF-024 | C | APPLIED | Section 7 Schema and transitions; FR-024; FR-026 | Store-level `consumed_log` keeps reset `consumed_at` values so `reset` cannot bypass the day cap. |
| PF-025 | C | APPLIED | FR-014 | Per-launch order fixed; it is the "launch steps" of FR-001 (panel conflict note). |
| PF-026 | M | MERGED-INTO PF-043 | FR-027 | Panel conflict note: PF-043's sentence includes PF-026's validity rule. |
| PF-027 | M | APPLIED | FR-004; exit table row 4 | 100 or more results, or a repeated `number`, exits 4 (`truncated`, `discovery_duplicate`). |
| PF-028 | M | APPLIED | FR-020; NFR-006 | Rotation keeps `.1` to `.4`; the NFR-013 helper reads all. |
| PF-029 | M | APPLIED | FR-016; FR-023 | Pipeline count fix: no stamping after the launch or for `budget_exhausted`; a second candidate is never reached. |
| PF-030 | M | APPLIED | FR-014; FR-015; FR-021 | Confirmed success needs a non-empty operation ID; exit 0 without one is `unknown`. |
| PF-031 | m | DEFERRED | FU-11 | A pruning rule needs a design choice about evidence retention; recorded as follow-up. |
| PF-032 | M | APPLIED | NFR-011; Section 7 Store form | Lower version migrated under the lock; only a higher or unknown version exits 6. |
| PF-033 | M | APPLIED | FR-009; Section 8 Tests; Section 12 | Verified the marker in `templates/claim-comment.md:23` and `refs/claim.md:29`; contract test `test_marker_contract.py` added. |
| PF-034 | M | APPLIED (modified) | FR-013 | The literal value is not written (no model name may appear in the spec); `ORCA_AGENT` is defined by reference to the seed brief and pinned by a unit test. |
| PF-035 | M | APPLIED (modified) | Section 3 Own login and Claimed; FR-002; R16; A-006 | 300 s skew tolerance [PROPOSAL] and `clock_skew`; the `Date` header is read from `gh api user --include`, since `gh issue list` exposes no headers. |
| PF-036 | M | APPLIED | Section 3 Eligible issue | Local-first check order; carries PF-004's state rule. |
| PF-037 | M | APPLIED | FR-019 | Dry-run shadow state in `<state_dir>/dry-run.json`, never read by a real cycle. |
| PF-038 | M | APPLIED | Section 1 Deployment gate; T10 | No cron entry before the owner-run live test replaces every `_assumed_shape` fixture. |
| PF-039 | m | APPLIED | Section 8 Gates | Trivial: `make sync-dev` listed as a preparation step. |
| PF-040 | C | APPLIED | NFR-009; Section 8 Budget arithmetic; FR-011 | Pipeline count fix: 35-call cap incl. pages and re-read (3 reserved); worst cycle 37 calls, 444 an hour, 8.88%. |
| PF-041 | M | APPLIED | NFR-014; Section 8 Modules | Clock Protocol (`now()`, `monotonic()`) in `cycle.py`; every time read goes through it. |
| PF-042 | M | APPLIED | Section 7 Time windows; FR-001 | Half-open windows; lease and `pending_orphan` sweep over every entry at cycle start. |
| PF-043 | C | APPLIED | FR-027; T13 | Approvers file checks (regular file, own UID, not group/other-writable, valid IDs) before any `gh` call, via `check-config`'s validator. |
| PF-044 | M | APPLIED | Section 1 Deployment gate; Section 8 runbook step 9 | Live-test record `docs/designs/issue-watcher-live-test.md` required. |
| PF-045 | M | APPLIED | FR-017 | Lock opened with `O_NOFOLLOW`; a non-regular or foreign lock exits 6. |
| PF-046 | m | APPLIED | FU-2 | Trivial: cron has six fields, seconds first. |
| PF-047 | m | NOTED | Section 8 runbook | Not trivial (restructures the runbook); steps 3, 7 and 9 stay separate. |
| PF-048 | m | DEFERRED | FU-12 | The local-filesystem allow-list needs per-host Coder facts; recorded as follow-up. |

## Counts

| Decision | CRITICAL | MAJOR | MINOR | Total |
|---|---|---|---|---|
| APPLIED (incl. 2 modified: PF-034, PF-035) | 11 | 26 | 4 | 41 |
| MERGED-INTO | 1 | 1 | 0 | 2 |
| DEFERRED | 0 | 0 | 2 | 2 |
| REJECTED | 0 | 0 | 0 | 0 |
| NOTED (minor, not applied) | 0 | 0 | 3 | 3 |
| Total | 12 | 27 | 9 | 48 |

Every CRITICAL and MAJOR finding is resolved (applied or merged into the finding that carries it).

## Conflicts and which finding wins

- PF-004 vs PF-036 (Section 3 Eligible issue): PF-036's ordering wins; PF-004's state rule replaces its "no entry with `launches > 0`" clause.
- PF-003 vs PF-025: no conflict in substance; PF-025's per-launch list is the "launch steps" of PF-003's cycle order. FR-001 also gains PF-013, PF-042 and PF-018 steps.
- PF-026 vs PF-043 (FR-027): PF-043 wins and carries PF-026's validity rule.
- PF-034 vs the no-model-name rule: the rule wins; the value is defined by reference.

## Ids added, renumbered or removed

- FR and NFR ids: none added, renumbered or removed (FR-001..FR-029, NFR-001..NFR-014; all referenced ids exist, none duplicated).
- Follow-up ids added: FU-11 (tombstone bound, PF-031), FU-12 (local-filesystem allow-list, PF-048).
- New names (not ids): store field `consumed_log`; entry field `approved_at`; file `dry-run.json`; verb `reset --rate-limit`; Section 7 "Time windows" paragraph; Section 8 "Reason codes" table with names marked † as [PROPOSAL]; tests `test_marker_contract.py` and `test_find_orca_parity.py`.

## Residual inconsistencies

- FR ids are not sequential by position: FR-022 to FR-025 sit between older requirements, kept to preserve source traceability.
- The reason-code names marked † are new [PROPOSAL] names, not taken from a source.
- `pending_orphan` and `claim_not_observed` exit 0 and surface only through `status`; this is an interpretation of the source, not stated there.
- `ORCA_AGENT`'s value exists only by reference to the seed brief (PF-034 modified).
- PF-016, PF-019 and PF-047 are noted, not applied; the spec still retries a prompt `ValueError` as `failed`.
- The repository name IronbellyOrg/IronClaude contains the substring "claude"; a whole-word, case-insensitive grep for the model names returns zero hits.
- Per-paragraph HTML Source comments from the merged draft are kept because Section 12 cites their ruling ids.
