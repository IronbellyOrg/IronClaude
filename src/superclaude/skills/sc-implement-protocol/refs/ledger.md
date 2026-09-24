# Ledger grammar

One markdown file per run. Append-only. UTF-8, `\n` endings, no wrapping of record lines. Do not `git add` the ledger.

## Location

Default: `.dev/implement/<slug>/progress.md`

- `<slug>` = basename of the source path without extension, lowercased, non-`[a-z0-9_-]` → `-`, trimmed, max 64 chars.
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
^# implement ledger — source: \S+ — created: [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$
```

## Start line (once per task, before edits)

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
- `<ev-list>` = comma-separated evidence tokens (no spaces): `rel/path:line`, `rel/path:start-end`, `T{i}.AC{k}`, `T{i}.AC{k}@rel/path:line`
- `<lx>`,`<tx>` ∈ `pass` | `fail` | `skip`
- `<sx>` ∈ `pass` | `fail` | `skip` | `unrelated-red`
- `<file-list>` = comma-separated repo-relative paths (no spaces)

```
^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=([^ ]+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=([^ ]+)$
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

## Negative (must fail the verdict regex)

```
Task 1: done
```
