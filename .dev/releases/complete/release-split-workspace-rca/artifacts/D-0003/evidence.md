# D-0003 Evidence — T01.03 Append `.claude/skills/*-workspace/` to `.gitignore`

**Date:** 2026-05-13
**Roadmap Item:** R-003
**Source:** FR-L2.6

## Change

Appended to `/config/workspace/IronClaude/.gitignore` (end of file):

```
# Skill eval workspaces must live in .dev/eval-workspaces/ -- see .dev/README.md
.claude/skills/*-workspace/
```

## Verification

### Probe directory (must be ignored)

```
$ mkdir -p .claude/skills/_probe-workspace
$ git check-ignore -v .claude/skills/_probe-workspace/
.gitignore:117:.claude/	.claude/skills/_probe-workspace/
exit=0
$ git status --short .claude/skills/_probe-workspace/
(empty — directory is ignored, not listed as untracked)
$ rmdir .claude/skills/_probe-workspace
```

`git check-ignore` exits 0 → probe path is ignored (acceptance criterion met).
The reporting line cites `.gitignore:117:.claude/` because the broader `.claude/`
entry (already present pre-change) matches first; our new pattern remains an
explicit defense-in-depth guarantee that survives any future relaxation of the
broader rule and documents intent via its comment.

### Legitimate skill directory (must NOT be ignored)

```
$ git check-ignore -v .claude/skills/sc-tasklist-protocol/
exit=1
$ git ls-files .claude/skills/sc-tasklist-protocol/ | head -3
.claude/skills/sc-tasklist-protocol/SKILL.md
.claude/skills/sc-tasklist-protocol/rules/file-emission-rules.md
.claude/skills/sc-tasklist-protocol/rules/tier-classification.md
```

Exit 1 → not effectively ignored; the directory's files are tracked and remain so.

### Pattern-only behavior (no-index, ignores tracked status)

```
$ git check-ignore -v --no-index -- .claude/skills/foo-workspace/
.gitignore:117:.claude/	.claude/skills/foo-workspace/
exit=0
```

The new pattern co-exists with the existing `.claude/` pattern; both would match
a workspace path, but only tracked skill directories like
`sc-tasklist-protocol/` remain in the repo because git preserves tracked files
regardless of `.gitignore`.

## Acceptance Criteria Status

- [x] `.gitignore` contains the literal pattern `.claude/skills/*-workspace/`.
- [x] `git check-ignore .claude/skills/_probe-workspace/` exits 0.
- [x] `git check-ignore .claude/skills/sc-tasklist-protocol/` does not match (existing skill remains tracked).
- [x] Probe commands and outputs captured in this file.

## Artifact

- Modified file: `/config/workspace/IronClaude/.gitignore` (appended 2 lines at EOF).
