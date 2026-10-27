# D-0015 — Evidence: AC4 CLAUDE.md Pointer Resolution

**Task:** T05.04 — AC4 test: grep CLAUDE.md pointers resolve to existing files
**Roadmap Item:** R-015
**Phase:** 5 (Acceptance Validation)
**Date:** 2026-05-13
**Result:** **PASS**

## 1. Grep against `CLAUDE.md`

Command (verbatim, run from repo root `/config/workspace/IronClaude`):

```
grep -nE 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md
```

Output:

```
51:KNOWLEDGE.md             # Accumulated insights
233:**KNOWLEDGE.md** - Accumulated insights and troubleshooting
```

Exit code: `0`.

Both matched lines reference `KNOWLEDGE.md`. Zero matches for
`PLANNING.md` or `TASK.md`.

Captured at `D-0015/grep-output.log`.

## 2. Per-pointer match counts

```
PLANNING.md matches: 0
TASK.md matches: 0
KNOWLEDGE.md matches: 2
```

Captured at `D-0015/match-counts.log`.

## 3. File existence checks

```
$ test -f KNOWLEDGE.md ; echo $?
0

$ test -f PLANNING.md ; echo $?
1

$ test -f TASK.md ; echo $?
1

$ ls -la KNOWLEDGE.md
-rw-r--r-- 1 abc abc 5563 May 13 03:04 KNOWLEDGE.md
```

`KNOWLEDGE.md` exists (exit 0). `PLANNING.md` and `TASK.md` do not
exist (exit 1) — this is expected and **does not** affect AC4, because
neither name appears in the grep output.

Captured at `D-0015/test-f-output.log`.

## 4. Acceptance criteria — pass matrix

| AC item | Expected | Observed | Pass? |
|---------|----------|----------|-------|
| Grep shows only `KNOWLEDGE.md` matches | true | true (2 lines, both `KNOWLEDGE.md`) | PASS |
| Zero `PLANNING.md` matches in grep | true | `grep -cE 'PLANNING\.md' = 0` | PASS |
| Zero `TASK.md` matches in grep | true | `grep -cE 'TASK\.md' = 0` | PASS |
| `test -f KNOWLEDGE.md` exit 0 | true | exit 0 | PASS |
| Outputs captured in `D-0015/` | true | `grep-output.log`, `match-counts.log`, `test-f-output.log`, `evidence.md` | PASS |
| Aligned with SC-004 | true | every surviving pointer resolves to a real file | PASS |

## 5. SC-004 mapping

Source-roadmap SC-004: documentation pointers in `CLAUDE.md` resolve
to existing files. The only doc pointer matched by the AC4 regex
(`KNOWLEDGE.md`) resolves to `KNOWLEDGE.md` at the repo root. **SC-004
is satisfied.**

## 6. Overall

**PASS** — AC4 holds. T05.04 acceptance criteria are met. T01.02
pointer repair is intact (no dangling `PLANNING.md` / `TASK.md`
references survive in `CLAUDE.md`), and the one surviving pointer
(`KNOWLEDGE.md`) resolves to an existing file.
