# T01.02 -- Evidence: Repair broken PLANNING.md/TASK.md pointers in CLAUDE.md

## Target file
`/config/workspace/IronClaude/CLAUDE.md`

## Pre-condition check
- `KNOWLEDGE.md` exists at repo root: PASS
- `PLANNING.md` does not exist at repo root: PASS
- `TASK.md` does not exist at repo root: PASS

## Edits applied
1. Project-structure block (former lines 51-53): removed `PLANNING.md` and `TASK.md` rows; retained `KNOWLEDGE.md`.
2. Key Documentation Files section (former lines 225-227): removed `PLANNING.md` and `TASK.md` rows; retained `KNOWLEDGE.md`.

## Verification commands
```
$ grep -E 'PLANNING\.md|TASK\.md' /config/workspace/IronClaude/CLAUDE.md
# (no output)
$ echo $?
1

$ grep -c 'KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md
2
$ echo $?
0
```

## Acceptance criteria status
- [x] `grep -E 'PLANNING\.md|TASK\.md' CLAUDE.md` exits status 1 (no matches).
- [x] `grep 'KNOWLEDGE\.md' CLAUDE.md` exits status 0 (preserved).
- [x] Edits scoped only to the two ranges identified by content match.
- [x] Diff captured at `artifacts/D-0002/clauded.diff`.

## Diff artifact
- Path: `.dev/releases/current/release-split-workspace-rca/artifacts/D-0002/clauded.diff`
- Generated via: `git diff CLAUDE.md`
