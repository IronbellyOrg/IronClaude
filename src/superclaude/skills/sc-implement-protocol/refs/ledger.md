# Ledger grammar

One markdown file per run. Append-only. UTF-8, `\n` endings, no wrapping of record lines. Do not `git add` a legacy ledger under `.dev/implement/`. A managed package's ledger (`<pkg>/progress.md`) sits under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).

## Location

Default: `.dev/implement/<slug>/progress.md`

- `<slug>` = `{prefix}-{hash8}` (see SKILL.md Wave 0 step 3/5): prefix from basename or prompt (max 24 slug-chars); hash8 from SHA-256 of the full prompt or absolute path. Same source resumes; distinct sources never share a directory.
- Create the directory if missing.
- `--ledger <path>` overrides. Must live under `.dev/implement/` or STOP `E-LEDGER-PATH`.
- Not next to the spec. Not `.claude/`. Not `docs/generated/`.
- Re-invoke on the same source reuses this path.

## Header (line 1 only)

```
# implement ledger — source: <abs-or-repo-relative-path> — created: <ISO-8601>
```

`<ISO-8601>` is `YYYY-MM-DDTHH:MM:SSZ`.

```
^# implement ledger — source: .+ — created: [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$
```

Path may contain spaces. The delimiter before the timestamp is ` — created:`.

## Start line (once per task, before edits)

On resume, if a start line exists and the task is not `complete`, reuse that sha. Do not append a second start line.

```
T<id>: start sha=<40-hex|nogit>
```

```
^T([0-9A-Za-z.-]+): start sha=([0-9a-f]{40}|nogit)$
```

## Verdict line

```
T<id>: <status> verdict=<verdict> ac=<ac-list> evidence=<ev-list> extras=lint:<lx>,typecheck:<tx>,test:<sx> files=<file-list>
```

- `<status>` ∈ `complete` | `blocked`
- `<verdict>` ∈ `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`
- `<ac-list>` = comma-separated `T{i}.AC{k}` (no spaces)
- `<ev-list>` = comma-separated evidence tokens. Paths **may contain spaces**. The field ends at ` extras=lint:`. Tokens: `rel/path:line`, `rel/path:start-end`, `T{i}.AC{k}@rel/path:line`. Bare `T{i}.AC{k}` is not sufficient for `compliant`. Do not put commas in paths.
- `notes@<path>:<start>-<end>` = evidence token pointing at the task's notes file (`refs/qa.md`); never an AC citation. Managed form: `notes@./artifacts/retries/T<id>/notes.md:<a>-<b>`.
- `<lx>`,`<tx>` ∈ `pass` | `fail` | `skip`
- `<sx>` ∈ `pass` | `fail` | `skip` | `unrelated-red`
- `<file-list>` = comma-separated repo-relative paths (paths may contain spaces; do not insert spaces after commas)

```
^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=(.+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=(.+)$
```

`complete` on the verdict line **only if** `verdict=compliant`. `compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`). Otherwise status MUST be `blocked` until an operator Ruling + a follow-up complete line.

## Ruling line (user-authorized, executor-recorded)

```
T<id>: Ruling: <what> — <why> — <cost-if-wrong>
```

Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`.

```
^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$
```

## Post-ruling complete line

After a valid operator Ruling:

```
T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... extras=... files=...
```

Legal **only** when a matching `T<id>: Ruling:` line exists above it, after the latest blocked record. Preserve all verdict fields, not only the verdict label. A later blocked record or new start invalidates prior acceptance. A changed accepted finding/outcome requires new user confirmation; do not reuse the old Ruling. Legacy records with a Ruling before the first verdict remain readable; that first complete verdict binds its scope.

## Retry and halt records

Two kinds for the escalating retry ladder (`refs/retry.md`): one `retry` kind with three steps, and `halt`. They are part of this main grammar, legacy and managed alike.

<!-- ledger-grammar-block: record forms -->
```
T<id>: retry n=<3|4|5> step=open checkpoint=<40-hex tree> tier=<ladder entry name|unknown>
T<id>: retry n=<3|4|5> step=revert brief=<brief path> supersedes=<T<id>_brief-<n-1>.md|none>
T<id>: retry n=<3|4|5> step=review
T<id>: halt review=<2|3|4|5> reason=<reason>
```

<!-- ledger-grammar-block: regexes -->
```
^T([0-9A-Za-z.-]+): retry n=([345]) (?:step=open checkpoint=([0-9a-f]{40}) tier=([A-Za-z0-9_]+)|step=revert brief=(\S+) supersedes=(T[0-9A-Za-z.-]+_brief-[34]\.md|none)|step=review)$
^T([0-9A-Za-z.-]+): halt review=([2-5]) reason=([a-z][a-z-]*)$
```

Meaning of each step:

- `step=open` is written right after the failed attempt's `blocked` line and before any other ladder action. It is the durable feature marker a pre-upgrade ledger cannot contain, and it records the checkpoint tree sha and the executor's rung name (`tier=`).
- `step=revert` records the brief and its `supersedes=` field, written after the brief and before the revert.
- `step=review` is written after attempt n is implemented and before its review, so a crash or `reviewer-down` re-runs only the review.

Semantic rules: for `step=revert`, the brief basename is `T<id>_brief-<n>.md`, where the id equals the line's task id and n equals the line's n; `supersedes` is `none` iff n = 3, else `T<id>_brief-<n-1>.md`. Brief 5 supersedes `T<id>_brief-4.md` even though it is built from the escalation-2 runner-up. A managed brief path is `./artifacts/retries/T<id>_brief-<n>.md` with no `..`; a legacy brief path is repo-relative, `.dev/implement/<slug>/retries/T<id>_brief-<n>.md`. `_` is outside the id class `[0-9A-Za-z.-]`, so the name splits unambiguously. For `step=open`, the protocol writes in `tier=` only the canonical name of the executor's rung in the active ladder or `unknown`; the regex accepts any `[A-Za-z0-9_]+`.

Placement rules: `step=open` for n follows the `blocked` line of attempt n-1; `step=revert` follows `step=open` of the same n; `step=review` follows `step=revert` of the same n; a verdict line follows `step=review`; a `halt` follows a `blocked`, a `retry step=open` or a `retry step=revert` line; after a `halt`, the task gets only operator `Ruling:` lines, the post-ruling `complete` that Resume row R writes, operator-review `blocked` and `halt` records (Resume). Operator `Ruling:` lines may appear between any two records.

Halt reason: open class `[a-z][a-z-]*`, with the legal list in `refs/retry.md` (Halts and transient stops). A closed enum in the parser turns a documentation slip into an append-only ledger that can never be repaired. `review=` is the closed range `[2-5]`, because attempts are numbered 2-5 when they can fail into a halt. The rule that gives k, the failed attempt, is in `refs/retry.md`.

## Final review line (optional)

```
FINAL: <pass|issues> evidence=<ev-list>
```

## Resume

```
if last line does not match header|start|verdict|ruling|retry|halt|FINAL regex → E-LEDGER-CORRUPT
parse lines in order
for each id in T1..TN (source order):
  if no line for id → resume here
  if latest status for id is not complete → resume here
  if latest status is complete → skip
first such id wins
if all complete → run FINAL unless --skip-final-review or FINAL already present or N=1
```

The completion rules in this section are **legacy-ledger** rules; managed packages follow the Managed-package extension below.

`--resume` is implicit when a matching ledger exists. If the ledger is missing, write the header before the first edit. If all tasks are `complete` **and** FINAL is already present (or N=1, or `--skip-final-review`): STOP `already complete: <ledger path>`. If all tasks are `complete` and FINAL is still due: run FINAL, then stop. Do not skip a pending N>1 whole-list review.

Trust ledger + git history after compaction. Do not ask the user to paste prior chat.

### Per-task resume table

Definitions, over the task's records after its latest `start`: "Last record" = the last task record, ignoring ineligible Rulings. "Latest verdict" = the last `complete` or `blocked` line. A `T<id>: Ruling:` line is eligible only under the Ruling eligibility rule in `refs/retry.md`. Before any row except Row 1 runs for a task with a tree `start`, every `r<k>-<j>` ref of the task is re-pinned from its recorded tree (review header or repair `applied tree=` line, `refs/qa.md`), so Rows V, S, H, B and X re-pin as well.

Ledgers written before the change resume through the existing rows. Findings with no recorded tree get `origin=unknown`, and absent repair files for the current `start` mean both repairs are unspent.

Precondition: one `/sc:implement` invocation writes a given ledger at a time; there is no lock.

Task selection stays as the pseudo-code above; this table replaces only the per-task dispatch (the "resume here" step). The table applies to legacy and managed ledgers alike: the completion rules above are scoped to legacy ledgers, so the managed dispatch line below ("first non-complete task") routes to this table. In every row, k is the k-rule value (`refs/retry.md`).

First match wins; the row order is part of the rule:

| Row | Condition | Action |
|---|---|---|
| 1 | Latest verdict is `complete` | Skip. Delete the Q0 pin and checkpoint refs if they still exist; keep sweep refs. Also delete the task's `r<k>-<j>` refs. |
| R | An eligible Ruling with no `complete` after it | Append the post-ruling `complete` with the latest `blocked` line's verdict unchanged (Post-ruling complete line), with no review, then row 1. |
| P | Latest verdict is `blocked`, and the task has no `retry` and no `halt` record | One fresh operator review of the tree as it stands, nothing reverted. `compliant` → `complete`. Otherwise append `blocked` and `halt review=2 reason=operator-review` → STOP `E-HALT-QA`. |
| H | A `halt` record exists | If the last record is a `blocked` after the latest `halt`, append `halt review=<k> reason=<r>` with r = `operator-review` → STOP. Otherwise one fresh operator review of the tree as it stands: `compliant` → `complete`; else `blocked`, then `halt review=<k> reason=<r>` with r = `operator-review` → STOP `E-HALT-QA`. |
| V | Last record is `retry n=<n> step=review` | If a `repair-<n>-<j>.md` for the current `start` exists, resume the repair (`refs/retry.md`, Repair round). Otherwise: Re-run only the review of attempt n (fresh reviewer). `compliant` → Q6-Q8; otherwise the Repair round decides as an uninterrupted run would, then procedure step 0 with k = n. |
| X | Last record is `retry n=<n> step=revert` | Run `sc_retry_revert` directly: its ledger binding and guards (tail, tree, HEAD, evidence) are the re-check, and exit 2 maps to the halt after any move-back or keep of failed-attempt artifacts (`refs/retry.md`, The revert). Otherwise the revert re-runs (idempotent: fresh `now`, create-only sweep), then procedure step 7. |
| O | Last record is `retry n=<n> step=open` | Re-check the ladder conditions (`refs/retry.md`, When the ladder runs), re-pin the checkpoint ref to the recorded sha and every `r<k>-<j>` ref from its recorded tree, then continue at procedure step 2. n = 3, 4: advisers re-spawned (procedure step 4). n = 5: escalation 3 runs again (no adviser; `T<id>_brief-5.md` rewritten). |
| B | Last record is a `blocked` line and the task has a `retry` record | k from the k rule (here the n of the latest `retry`, because this `blocked` follows its `step=review`). k = 5 → append `halt review=5 reason=ladder-end` → STOP. Otherwise continue at the ladder-condition checks for this k, then procedure step 1. |
| S | Start line only | If a `repair-2-<j>.md` for the current `start` exists, resume the repair (`refs/retry.md`, Repair round). Else A1, as today. |

## Examples (must match)

Start:

```
T1: start sha=0123456789abcdef0123456789abcdef01234567
```

Compliant complete:

```
T1: complete verdict=compliant ac=T1.AC1 evidence=src/foo.py:12,T1.AC1 extras=lint:skip,typecheck:skip,test:skip files=src/foo.py
```

Compliant complete with notes (open minors recorded in the notes file):

```
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3,T1.AC4 evidence=T1.AC1@docs/user-guide/memory-system.md:12,T1.AC2@docs/user-guide/memory-system.md:40,T1.AC3@docs/memory/README.md:8,T1.AC4@docs/memory/README.md:21,notes@.dev/implement/03-memory-docs-f5865990/retries/T1/notes.md:1-3 extras=lint:skip,typecheck:skip,test:skip files=docs/user-guide/memory-system.md,docs/memory/README.md
```

Blocked missing:

```
T2: blocked verdict=missing ac=T2.AC1,T2.AC2 evidence=T2.AC1 extras=lint:pass,typecheck:skip,test:unrelated-red files=src/bar.py
```

Executor-recorded Ruling after the explained scope, reason and cost, followed by the user's "yes, accept T2 as explained":

```
T2: Ruling: accept T2 missing pagination; user confirmed in current conversation "yes, accept T2 as explained" — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
```

The earlier operator-written form (`T2: Ruling: drop pagination — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated`) remains valid.

Retry open:

```
T1: retry n=3 step=open checkpoint=0123456789abcdef0123456789abcdef01234567 tier=T2_Model02
```

Retry revert:

```
T1: retry n=3 step=revert brief=.dev/implement/notes-0a1b2c3d/retries/T1_brief-3.md supersedes=none
```

Retry review:

```
T1: retry n=3 step=review
```

Halt:

```
T1: halt review=2 reason=budget
```

## Managed-package extension (`refs/managed-workspace.md`)

Managed ledgers (`<package>/progress.md`) reuse every record above unchanged and add three record kinds. Legacy ledgers never contain them.

```
^PLAN: sha256=[0-9a-f]{64} source_sha256=[0-9a-f]{64}$
^FINAL: (pass|issues) evidence=.+ state=[0-9a-f]{64}$
^ARCHIVE: (start|failed|Ruling:) .+$
```

- Line 2 is the `PLAN:` pin. Append another `PLAN:` line only **before** the first `T<id>: start`; after it, a plan/source hash mismatch is `E-PLAN-CHANGED`.
- `evidence=` tokens may be package-relative: `./artifacts/<file>:<line>`.
- A log token cites the line that shows the outcome (a pytest summary such as `48 passed in 0.16s`, ruff's `All checks passed!`), not a banner and not the trailing `rc=` line; one token per outcome when a log covers several commands.
- A managed `FINAL:` carries the helper's `state=` digest and must be the last record before the helper's own `ARCHIVE: start id=<id> token=<hex>` line. Any later `PLAN`/`T`/`ARCHIVE` record makes it stale: run a new FINAL on every archive attempt. `ARCHIVE: failed id=<id> token=<hex> reason=<code>` records a refused attempt.
- Legacy `ARCHIVE: Ruling: <what naming T-ids> — <why> — <cost-if-wrong>` records remain readable but are optional. A matching task Ruling is sufficient for ordinary archiving of unchanged accepted work; never demand duplicate approval. Neither form waives FINAL or authorizes commit, PR, merge or release.
- Resume dispatch for managed packages: location check → pin check → first non-complete task → the per-task resume table (Resume) → all complete = active all-complete → archive gate. "Already complete" is reported only after the helper answers `already-archived`.

```
# implement ledger — source: ./TASK-WF-authLogin-20261001-063000.md — created: 2026-10-01T06:30:00Z
PLAN: sha256=0000000000000000000000000000000000000000000000000000000000000000 source_sha256=1111111111111111111111111111111111111111111111111111111111111111
T1: start sha=0123456789abcdef0123456789abcdef01234567
T1: complete verdict=compliant ac=T1.AC1 evidence=src/foo.py:12,T1.AC1@./artifacts/t1-test.log:3 extras=lint:skip,typecheck:skip,test:pass files=src/foo.py
FINAL: pass evidence=src/foo.py:12 state=2222222222222222222222222222222222222222222222222222222222222222
ARCHIVE: start id=TASK-WF-authLogin-20261001-063000 token=0123456789abcdef
```

## Negative (must fail the verdict regex)

```
Task 1: done
```
