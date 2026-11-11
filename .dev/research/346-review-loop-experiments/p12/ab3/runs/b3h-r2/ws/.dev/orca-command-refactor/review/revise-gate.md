# Revise: gate review of orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- brief: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (the Revise brief, Values: `{{IDS}}` only)
- input report: `.dev/orca-command-refactor/review/gate.md` (`review: 1 of 3`, verdict FAIL, GATE prompt)
- IDS: RA-01, RA-02, RA-03, RA-04 (`gate.md:166-168`, Reviser brief: "Blocking ids: RA-01, RA-02, RA-03, RA-04.")
- reviser: claude-haiku-5-5
- scope: only the four blocking findings. Medium (RA-05 to RA-18) and minor (N-01 to N-04) findings were not edited (`gate.md:170`).

## Byte accounting

| Item | sha256 | bytes | lines |
|---|---|---|---|
| Before (gate candidate) | `06cb4bcd39e29ea26abacd7521abf23c5e125f1cefda82fb1736f725a01d24b0` | 60408 | 290 |
| After (this revision) | `d33b89a08efc2ef08e5a0449828d8b35251424cc7d54958dac98f929b1383529` | 60936 | 290 |
| Net | | +528 | 0 |

Per finding id (bytes of the replaced text; each edit replaces one passage with one passage, so added and deleted are measured on the old and new strings):

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| RA-01 | 305 | 105 | +200 |
| RA-02 | 204 | 103 | +101 |
| RA-03 | 221 (135 + 86, two passages) | 125 (82 + 43) | +96 |
| RA-04 | 209 | 78 | +131 |
| Total | 939 | 411 | +528 |

The net total equals the file delta (60936 - 60408 = 528). Five lines changed: spec:84, spec:142, spec:159, spec:199, spec:201. No other line was touched and the spec remains 290 lines.

## Findings

| Finding | Status | Where (after revision) | Change and reason |
|---|---|---|---|
| RA-01 (AC-0.4 cannot pass in P0) | applied | `spec:199` (AC-0.4) | Step 3 is applied to the command's existing report file (the "Report today" column of section 3.1, `spec:81-83`), not the WC-4 contract, and its outcome is checked against that file's status under WC-5. Step 4 uses the same existing report file, as before. The P0 check no longer requires a contract that P1 creates (`spec:159`, `spec:200`). |
| RA-02 (AC-1.2 applies the live check to `load`) | applied | `spec:201` (AC-1.2) | `load` is excluded from AC-1.2. The gate's stated reason holds: `load` is never its own Task and writes no contract (`spec:112`, `spec:62`). AC-1.1 already excludes `load` (`spec:200`), so the two checks now agree. The gate offered "exclude" as one option and this revision takes it; no new check was added. |
| RA-03 (brainstorm in section 3.1 but in no phase) | applied | `spec:84` (brainstorm row, last column); `spec:159` (P1 row) | Brainstorm is added to P1 as "flag and `## Unattended mode` section only", the additive option the gate names (`gate.md:46`). The 3.1 row no longer says "None" for the P1 flag and section. The row's evidence is unchanged; it still cites `inventory/commands-a.md:39` (brainstorm ready with default flags), which is consistent with an additive change. AC-1.1 (`spec:200`) and P1's "every command in sections 3.1 and 3.2" (`spec:159`) now both reach brainstorm. |
| RA-04 (section 5 says standalone behaviour does not change; SA-3 names a standalone change) | applied | `spec:142` (section 5 lead paragraph) | The "hard requirement on every phase" sentence now names its two exceptions: the adversarial contract path that SA-3 names (`spec:148`), and the documented defect fixes that SA-4 names (`spec:149`). SA-4 is named as well because its defect fixes also change standalone output, so leaving it out would keep the same contradiction. The nested `adversarial/adversarial/` path is the defect cited at `inventory/commands-a.md:35` and `inventory/commands-a.md:60-61`, which SA-3 (`spec:148`) already removes under SA-4. |

## Checks made

- The gate's citations for the four findings were checked against the inventory files: `inventory/commands-a.md:35`, `:39`, `:42`, `:44`, `:51`, `:60-61` exist and match the claims the gate and spec make about them (adversarial nested path at `:35` and `:60-61`; brainstorm ready with default flags at `:39`).
- The spec lines the edits depend on were re-read after editing: `spec:84`, `:142`, `:159`, `:199`, `:201` (grep output) and `spec:148-149` (SA-3, SA-4, unchanged).
- Each edit replaced a unique passage; each edit's old text was matched exactly once.
- Not checked: any citation into `src/`, `tests/` or `~/.claude/` (outside the workspace, marked UNVERIFIED in `gate.md:10`). The revision adds no new citation into those paths.

## Self-check on new text

- No new rule, mechanism or section was added beyond what a blocking finding calls for. Each added phrase cites its finding id: "(RA-01)", "(RA-02: ...)", "(RA-03)", "(RA-04)".
- The P0 and P1 scopes are unchanged apart from the brainstorm addition.
- No verdict or PASS is awarded. This output is the revision only; the re-review is for the loop to run.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| RA-03: add brainstorm to P1 | Add to a phase (additive flag and section); narrow AC-1.1 and P1 to exclude it | The gate lists both. Adding keeps AC-1.1 and P1's "every command in sections 3.1 and 3.2" as written, and the change is additive (SA-4). |
| RA-04: name SA-4 as well as SA-3 in the exception | Name SA-3 only (the gate's minimal option); name both | SA-4 also changes standalone content through defect fixes (`spec:149`), so naming only SA-3 would leave the same contradiction. |
| RA-02: exclude `load` rather than add a separate check | Exclude; add a separate check for `load` | The gate offered both. Exclusion is the smaller change and matches AC-1.1's existing exclusion (`spec:200`). |
| Edit only the five lines the four findings name | Also tidy related text (for example RA-09, RA-14) | The brief limits the revision to blocking ids and forbids editing Medium and minor findings (`gate.md:170`). |
