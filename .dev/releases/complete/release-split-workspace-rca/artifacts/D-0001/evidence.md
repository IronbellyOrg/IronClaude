# D-0001 — Evidence

**Task:** T01.01
**Deliverable:** `.dev/README.md`
**Produced:** 2026-05-13

## Produced Artifact
- [`.dev/README.md`](../../../../../README.md) (repo-root: `/config/workspace/IronClaude/.dev/README.md`)

## Verification commands & results

### 1. File exists
```
$ ls -la /config/workspace/IronClaude/.dev/README.md
-rw-r--r-- 1 abc abc <size> May 13 04:13 /config/workspace/IronClaude/.dev/README.md
```
Result: PASS — file present at repository root.

### 2. Verbatim FR-L2.4 rule present
```
$ grep -c "Workspaces, fixtures, harness code, and iteration outputs go under" /config/workspace/IronClaude/.dev/README.md
1
```
Result: PASS — rule string present exactly once. Full rule text in the README opens the document as a blockquote:

> Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`. Eval workspaces use `.dev/eval-workspaces/<skill-name>/`.

### 3. Subdirectory enumeration matches filesystem
```
$ ls /config/workspace/IronClaude/.dev/ | sort
README.md
benchmarks
evals
eval-workspaces
releases
research
resurrection-contracts
tasks
test-fixtures
test-sprints
```
README enumerates exactly the 9 non-README entries above. Result: PASS.

## Acceptance Criteria Mapping

| Criterion | Status |
|---|---|
| File `.dev/README.md` exists at repository root and contains FR-L2.4 rule verbatim | PASS (commands 1, 2) |
| Every existing subdirectory of `.dev/` enumerated with 1-line purpose | PASS (command 3 + README content) |
| Document committed in same change-set that introduces it | Pending commit (no orphan staging — to be bundled with rest of T01.01) |
| Reference link to `.dev/README.md` recorded here | PASS (link at top of this file) |
