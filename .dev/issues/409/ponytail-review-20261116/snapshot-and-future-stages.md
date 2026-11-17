# Ponytail review: snapshot export, schema, versioning promise and future-stage docs

Reviewer: ponytail-snapshot (lazy-senior lens, read-only on product code). Date: 2026-11-16. Branch 409-Phase2.
Reviewed live lines of: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/export.py`, `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/snapshot.schema.json`, `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/commands.py` (lines 196-240, 276-320, 355-370), `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_export.py`, `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_snapshot_schema.py`, the spec files `snapshot-export-schema.md` and `write-back-future-stage.md` under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/`, the TUIBBS review under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/`, and the owner decisions file.

## Summary

1. The owner asked for one thing: a versioned, additive-only JSON snapshot written by `export(view)`, with a schema test, so a read-only Go screen can read it later. The core of that is justified and small; keep it.
2. About half of export.py (lines 29-59 and 123-232, roughly 140 of 276 lines) plus a 158-line schema and about 700 test lines serve a consumer that does not exist (no Go code, no reader of `snapshot.json` anywhere in the repo). Most of that is the owner's request done faithfully; the real excess is a questions group nobody asked for, two extra collection fields, and production code that validates the schema at import only for tests.
3. The write-back document is a second copy of the TUIBBS review file (115 lines of near-duplicate text across two files) for a stage that needs a boundary change nobody has approved. Replace the copy with a pointer. Smallest honest cut: about 190 lines of tests, 55 lines of schema and code, 45 lines of docs, no loss of any redaction guarantee.

## What the owner asked for versus what exists

### Asked for (keep, can shrink slightly)

Source: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` item 5: "`export(view)` writes a versioned, additive-only JSON snapshot with a schema test, in release-1 scope, so a read-only Go screen inside TUIBBS can read it later." Item 4 says TUIBBS as staff platform is background only. Item 3 (write-back) is a future stage needing a boundary change.

| Owner-asked piece | Where it lives | Verdict |
|---|---|---|
| Versioned (`schemaVersion`) | export.py:23, schema.json:9 | Keep. |
| Additive-only rule | schema.json:4 (text only), spec doc rules | Keep as one sentence. UNVERIFIED that anything mechanically enforces it: the only freeze is the byte-level golden file `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/golden_release1_surface.json` and test_snapshot_schema.py:60. |
| `export(view)` writes JSON | export.py:185-232 | Keep. |
| Schema test | test_snapshot_schema.py (20 tests, 558 lines) | Keep the contract tests; see trim list. |
| Envelope + row fields listed in tuibbs-review/architecture-options.md:79-107 | export.py:37-59, 185-208 | Keep: this list is the owner-confirmed freeze. |

### Added on top (nobody asked, no acceptance criterion, no owner decision)

I grepped issue-body.md for snapshot/export/schema: its only export-related acceptance criterion is "readable ASCII/text exports" (line 79), which is the text record (`e` key, `--once`), not the JSON snapshot. The JSON snapshot has no acceptance criterion in issue-body.md; its only authority is owner decision item 5.

| Added piece | Evidence it was added | Lines |
|---|---|---|
| `questions` group in the snapshot (id, createdAt, ageSeconds, inWindow, window flags) | `snapshot-export-schema.md` never mentions questions (grep found no hit in that file); the group is in schema.json:65-94 and export.py:160-182, 209-210. Not in architecture-options.md:79-107 either. Added with the R2 question work (recent commits 1ae72e1a1, f104ca51a). | ~25 code, 30 schema, ~146 test lines |
| `collection.changedDuringRead`, `collection.duplicatesIgnored` (and `collected`) | Spec marks them "optional (additive)"; not in the owner-confirmed field list. `SnapshotMeta` fields view.py:178-181 are only read by export.py:211-217 (grep, no other reader). | 2-3 fields, ~6 lines across export/view/schema |
| `absentFields`, `orderUnknown`, `notReobserved` row flags | Spec "optional (additive)" observer flags; export.py:150-156, schema 152-154. Reasonable honesty features (they tell a consumer a UNKNOWN is a gap, not source text). Keep `absentFields`; the other two are low-cost. | ~8 lines |
| Row ordering rule written in the snapshot spec | Spec lines 70-74; code just uses `view.all_rows` (export.py:207). Costs no export code, but creates OQ-12. | docs only |
| Per-cycle automatic live write to `~/.local/state/superclaude/observe/snapshot.json` | commands.py:276-300, 355-369; spec "Write rule (PROPOSED)", destination still open (UX-OQ-4). Owner asked that the export exist, not that a file is rewritten every cycle with no reader. | ~12 lines + 2-3 tests |
| Schema loaded and `check_schema`-validated at import in production code | export.py:23-34, 29-34. `SCHEMA` has readers only in tests (grep: tests/observe/test_commands.py:34, test_snapshot_schema.py:15). | 8 lines of production code |
| "Options considered" table in the snapshot spec | snapshot-export-schema.md:80-91 duplicates tuibbs-review/architecture-options.md:49 | 12 doc lines |
| Write-back future-stage spec | write-back-future-stage.md (50 lines) duplicates tuibbs-review/write-back-stage.md (65 lines): same threat-model table, same gates 0-8, same "smallest first stage" | 50 doc lines |

Not extra, keep: `record_text` (export.py:62-120), `write_atomic`, `state_dir`, `record_path` (used by the `e` key and `--once`, a real user-visible behaviour and issue AC line 79).

## Fields with no reader

Method: Grep for `snapshot_json`, `snapshot_dict`, `snapshot.json`, `snapshot.schema` across the repo (excluding `.dev/`), and for Go files (`*.go`) mentioning "snapshot" (none found). Result: the only callers of `snapshot_json` are `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/commands.py:206` (writes the file), tests, and `tests/observe/release1_surface.py:54` (golden). Nothing reads `snapshot.json` back. So every field below has zero production readers today; the only readers are the schema tests. That is expected for "read later", so "no reader" alone is not a trim reason. The useful split is whether the owner's frozen list contains the field.

| Snapshot field (export.py line) | Reader today | In owner-confirmed list (architecture-options.md:79-107)? | Same data already shown to a user? |
|---|---|---|---|
| `schemaVersion`, `producer.*`, `cycle`, `generatedAt` (195-198) | tests only | yes | `generatedAt` in record header |
| `source.namespace/status/observedAt/error` (186-193) | tests only | yes | yes (freshness strip) |
| `page.hasMore/total/limit` (200-204) | tests only | yes | yes (collected/reported) |
| `scope`, `counts` (205-206) | tests only | yes | yes (COUNTS strip) |
| Row identity and state: `dispatchId, taskId, runId, workerState, dispatchStatus, terminalState, role, provider, hostKind, hostId, stage.worker, stage.dispatch, outcome, liveness.*, evidence.*, nextAction` (37-59) | tests only | yes (`stage.detail`/`activity` deliberately withheld) | yes (ledger and inspector) |
| `orderUnknown`, `notReobserved`, `absentFields` (150-156) | tests only | no (added, additive) | yes (row flags) |
| `collection.state`, `collection.collected` (211-217) | tests only | no | yes (partial-page notice) |
| `collection.changedDuringRead`, `collection.duplicatesIgnored` | tests only | no | UNVERIFIED whether the screen shows them; `SnapshotMeta` (view.py:178-181) is described as "values the JSON snapshot needs" (view.py:163) and grep shows no reader outside export.py |
| `questions.*` (160-182) | tests only | no, and absent from the spec doc | partly (question panel) |

Fields with no reader and no owner request: `collection.changedDuringRead`, `collection.duplicatesIgnored`, the whole `questions` group. Everything else traces to the owner's list or is a one-line honesty flag.

## Trim candidates (ranked)

Ranked by (risk of harm if wrong, low first) times (lines saved). No candidate touches redaction: every trim below either keeps the forbidden-key test (`test_snapshots_carry_no_forbidden_keys_words_or_fixture_input_values`, test_snapshot_schema.py:298) or removes a group that exports nothing sensitive in the first place.

### 1. Drop the `questions` group from the snapshot (largest, low risk)

- Where: export.py:160-182 and 209-210 (about 25 lines); schema.json:65-94 (30 lines); test_snapshot_schema.py:413-558 (about 146 lines, 8 tests: lines 448, 467, 481, 491, 506, 515, 530, 553 plus the helper at 415-445); small assertion edits in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_question_cap.py` (lines 84, 129, 134 read the snapshot's questions fields); `golden_release1_surface.json` needs regeneration (85 lines mention "questions", UNVERIFIED how many are in the snapshot part).
- Saved: about 55 production/schema lines and about 150 test lines.
- What depends on it: nothing reads it. The screen and the text record keep their own question panel (export.py:101-120 stays), so the user-visible `e` record and `--once` output do not change.
- Why safe: the spec's snapshot contract (snapshot-export-schema.md) never listed it, and the schema is additive-only, so it can return as a new optional group the day a Go screen needs it, with no version bump. Dropping it also removes the only place a question id, creation time and run id could leave the process in JSON form, which is a smaller attack surface by default.
- Risk: low. The risk is that a recent owner order (the 2026-11-11 and 2026-11-12 decisions files) requires the questions in the snapshot. I grepped both files for "snapshot" and found no hit; read of full text not done (UNVERIFIED). Check with the owner in one line before cutting, because commit f104ca51a "cite the owner-written pass record for the live questions read" is recent and may have been driven by a request for this group.

### 2. Stop validating the schema in production code (smallest diff, near-zero risk)

- Where: export.py:23-34 (the `resources`/`Draft7Validator` imports, `SCHEMA_PACKAGE`, `SCHEMA_FILE`, `SCHEMA`, `check_schema`) and the `jsonschema` import at line 18.
- Change: move the load and `check_schema` into a test helper (`/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/conftest.py`), and change the two imports at test_commands.py:34 and test_snapshot_schema.py:15. test_snapshot_schema.py:54-61 already reloads the packaged file itself.
- Saved: about 8 production lines and every `superclaude observe` start no longer imports `jsonschema` or parses the schema (`jsonschema` stays in pyproject.toml:39 because roadmap and eval use it). Adds about 4 test lines.
- Risk: very low. The "broken schema fails at import, not in the field" comment (export.py:32-33) is satisfied just as well by the existing test at test_snapshot_schema.py:61.

### 3. Collapse the write-back spec copy into a pointer (docs only, low risk)

- Where: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md` (50 lines). It repeats the threat-model table and gates 0-8 from `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/write-back-stage.md` (65 lines). Replace with about 6 lines: boundary change needed in two places, never in the snapshot, owner decision 3 still open, full design at the tuibbs-review path.
- Saved: about 44 lines; removes a place where the two copies can drift (they already differ in wording of the gates).
- What depends on it: about 20 `.dev/issues/409` files mention `snapshot-export-schema` or `write-back-future-stage` (grep list: SPEC.md, prd.md, ARCHITECTURE-SPINE.md, acceptance-tests.md, release-gates.md, and others). Keep the file name so those links stay valid; only shrink the body.
- Risk: low; it is documents with no code behind them. Do not delete the tuibbs-review files: they are the evidence trail.

### 4. Drop `collection.changedDuringRead` and `collection.duplicatesIgnored` (small, low risk)

- Where: export.py:211-217 (2 lines), schema.json:61-62, spec doc lines 43-44, and the two `SnapshotMeta` fields at view.py:180-181 with their fill at view.py:569-572, plus assertions in test_snapshot_schema.py:368-390 and the golden file.
- Saved: about 10 lines and 2 fields.
- Risk: low, but keep `collection.state` (COMPLETE/PARTIAL/MISMATCH): a consumer that cannot tell a partial row set from a complete one would show wrong data, which matches the issue's "make partial information explicit" criterion (issue-body.md line 78).

### 5. Make the live per-cycle snapshot write opt-in (judgment call, ask the owner)

- Where: commands.py:276-300 (`write_snapshots`, `written` counter), 355-369, `snapshot_path` export.py:255-256, tests test_commands.py:406-468.
- Change: write only when `--snapshot PATH` is given (this already works for `--once` and fixture mode, commands.py:232-233 and test_commands.py:167).
- Saved: about 12 lines and 2-3 tests. Also stops a default disk write to `~/.local/state/superclaude/observe/` every cycle with no reader.
- Risk: medium. It changes the proposed default (spec CD-6, destination still open per UX-OQ-4), and a Go screen would then need the observer started with the flag. Do this only if the owner agrees; otherwise leave as is. Not recommended before the owner answers.

### 6. Trim the snapshot spec doc (docs only)

- Delete "Options considered" (snapshot-export-schema.md:80-91, 12 lines; the same table exists in architecture-options.md:49) and replace the Ordering section (70-74) with one line: "Rows are in ledger order; a consumer sorts." That removes OQ-12 (see next section).
- Risk: low. The ordering section is currently ahead of nothing in code (export.py:207 uses `view.all_rows`); test at test_snapshot_schema.py:343 pins the current order, so keep that test or reword it.

### Do not trim

- `test_snapshots_carry_no_forbidden_keys_words_or_fixture_input_values` (test_snapshot_schema.py:261-338), the injection/sanitize test (test_export.py:115), the atomic write and 0600 tests (test_export.py:157-190), `absentFields` (separates a source value "UNKNOWN" from a gap), the `UNKNOWN` string rule, and the closed schema with `additionalProperties: false`. These are the redaction and honesty guarantees.
- The versioning promise itself (additive-only, bump on break) is one sentence in schema.json:4 and costs no code. It is the owner's request; keep it.

### Tally if candidates 1 to 4 and 6 are applied

About 55 lines production/schema, about 160 test lines, about 60 doc lines; zero change to the `e` key, `--once` text, or the redaction tests.

## Open questions this component is connected to

Source: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 427-433.

| OQ | Question | Verdict | Why |
|---|---|---|---|
| OQ-9 | Licence opinion before any Go screen reads the snapshot | Can be deferred without cost | Nothing reads the snapshot today; the opinion gates writing the Go screen, not the Python export. It stays open at no cost until a Go screen is actually proposed. Keep the one-line rule in the spec; do not add work. |
| OQ-10 | Does TUIBBS become the staff platform | Can be deferred without cost | Owner decision item 4 says background only. The snapshot is the same file whether or not TUIBBS is chosen. TUIBBS-scp review marks it refuted as a team platform today (tuibbs-review/summary.md), which is another reason not to build for it now. |
| OQ-11 | Write-back boundary change (issue 409 plus TUIBBS FR-X-13) | Can be deferred without cost, and nothing in the snapshot depends on it | The snapshot is one-way by construction and write-back lives in a later Go screen (write-back-future-stage.md line 35). If the write-back spec copy is shrunk to a pointer (trim 3), the question still lives in prd.md and the owner decisions file. The owner must answer it before any write-back build, not before R1. |
| OQ-12 | Which row order is authoritative for snapshot consumers | Disappears if trimmed (trim 6) | Code already writes ledger order (export.py:207). Declare "ledger order, consumers sort" and the question has no remaining content. If the order is kept as a contract, it needs an answer now, because it would then be frozen by the version promise. Cheapest answer: do not promise an order. |
| OQ-15 | Which `projection.stage.*` subfield drives change detection; may `stage.detail`/`stage.activity` enter the snapshot | Already answered for the snapshot by the code, needs no answer now | The snapshot spec (line 58) and export.py (no detail/activity in `_TEXT_FIELDS`, lines 37-57) withhold both, and the schema has no such keys; the forbidden-key test pins it. The change-detection half is a view/collector question, not a snapshot one. Leave the stricter rule in place; adding the fields later is additive. |

Related, not in the list: UX-OQ-4 (default snapshot destination). It disappears if trim 5 is taken, otherwise it is a small owner decision; no consumer waits on it.

## Not checked

- I did not run the test suite or measure test time; line and test counts come from Read and Grep only.
- UNVERIFIED: whether `tests/observe/golden_release1_surface.json` embeds the questions group in its `snapshot_json` part (85 lines mention "questions"; I did not parse it). Regeneration may be needed after trims 1 and 4.
- UNVERIFIED: full text of `owner-decisions-20261111.md` and `owner-decisions-20261112.md` (I only grepped for "snapshot" and found no hit); the 2026-11-12 file might require the questions group in the snapshot. Confirm before cutting trim 1.
- UNVERIFIED: whether `view.py` shows `coverage.total_changed` and `coverage.duplicates` on screen (trim 4); I only confirmed that `SnapshotMeta` has no reader besides export.py.
- Not read in full: the remaining spec files (SPEC.md, acceptance-tests.md, release-gates.md), `tuibbs-review/notes-1.md`, `notes-2.md`, `notes-3.md` (about 400 lines of raw notes, kept as evidence and not recommended for trimming), and tests in test_commands.py beyond the snapshot lines.
- Not checked: whether the packaged `snapshot.schema.json` is included in the built wheel (hatchling package data).
- Transport of the snapshot from the Coder host to a TUIBBS host remains unexamined in the sources (UNVERIFIED); nothing here changes that.
