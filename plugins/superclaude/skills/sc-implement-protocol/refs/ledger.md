# Ledger grammar

One markdown file per run. Append-only. UTF-8, `\n` endings, no wrapping of record lines. Do not `git add` the ledger.

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
- `<lx>`,`<tx>` ∈ `pass` | `fail` | `skip`
- `<sx>` ∈ `pass` | `fail` | `skip` | `unrelated-red`
- `<file-list>` = comma-separated repo-relative paths (paths may contain spaces; do not insert spaces after commas)

```
^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=(.+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=(.+)$
```

`complete` on the verdict line **only if** `verdict=compliant`. Otherwise status MUST be `blocked` until an operator Ruling + a follow-up complete line.

## Ruling line (operator-supplied only)

```
T<id>: Ruling: <what> — <why> — <cost-if-wrong>
```

Em dashes as shown (` — `). Three non-empty fields. Executor MUST NOT write this line.

```
^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$
```

## Post-ruling complete line

After a valid operator Ruling:

```
T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... extras=... files=...
```

Legal **only** when a matching `T<id>: Ruling:` line exists above it.

## Final review line (optional)

```
FINAL: <pass|issues> evidence=<ev-list>
```

## Resume

```
if last line does not match header|start|verdict|ruling|FINAL regex → E-LEDGER-CORRUPT
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

## Examples (must match)

Start:

```
T1: start sha=0123456789abcdef0123456789abcdef01234567
```

Compliant complete:

```
T1: complete verdict=compliant ac=T1.AC1 evidence=src/foo.py:12,T1.AC1 extras=lint:skip,typecheck:skip,test:skip files=src/foo.py
```

Blocked missing:

```
T2: blocked verdict=missing ac=T2.AC1,T2.AC2 evidence=T2.AC1 extras=lint:pass,typecheck:skip,test:unrelated-red files=src/bar.py
```

Ruling:

```
T2: Ruling: drop pagination — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
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
- A managed `FINAL:` carries the helper's `state=` digest and must be the last record before the helper's own `ARCHIVE: start id=<id> token=<hex>` line. Any later `PLAN`/`T`/`ARCHIVE` record makes it stale: run a new FINAL on every archive attempt. `ARCHIVE: failed id=<id> token=<hex> reason=<code>` records a refused attempt.
- `ARCHIVE: Ruling: <what naming T-ids> — <why> — <cost-if-wrong>` is operator-supplied only; the executor MUST NOT write it, and it never waives FINAL.
- Resume dispatch for managed packages: location check → pin check → first non-complete task → all complete = active all-complete → archive gate. "Already complete" is reported only after the helper answers `already-archived`.

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
