# Local git rehearsal of the release procedure (issue 826, Task 12)

Run with a temporary bare repository as `origin` (HEAD -> `refs/heads/integration`, branches `integration` and `master`) and a clone of it; the temporary folder was removed at the end. No GitHub call, no push to any real remote, no tag in the real repository. `git merge --no-ff` stands in for a GitHub merge commit: it has the same two-parent shape and does not prove `gh pr merge`.

Location guard: every rehearsal git command ran as `git -C <absolute temporary clone>` (the clone was `/tmp/rehearsal-826-joeqqaw_/clone`); `git rev-parse --show-toplevel` is logged with each check and must equal the clone; before every push `git remote get-url origin` printed the temporary bare repository (`/tmp/rehearsal-826-joeqqaw_/origin.git`).

Result: 29 of 29 entries passed; failed: none.

## 0. setup

- command: `bare origin /tmp/rehearsal-826-joeqqaw_/origin.git with HEAD -> refs/heads/integration; clone /tmp/rehearsal-826-joeqqaw_/clone; integration and master pushed`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
A=9e78b108761ccecb3883ab9a21415bc7afa7cecd
B, C on integration; reviewed head (integration tip) = cc75204a583001a568dbfc1497bc2f61c7c95582; master tip = 9e78b108761ccecb3883ab9a21415bc7afa7cecd
```

## 1. Step 2 precondition before the release merge (master is an ancestor of integration: exit 0 means go on)

- command: `git -C <clone> merge-base --is-ancestor origin/master origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 2. Step 2 precondition after the release merge, before the merge-back (exit 1 means the release was not merged back)

- command: `git -C <clone> merge-base --is-ancestor origin/master origin/integration`
- exit code: 1
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 3. Step 3: <merge-sha>^2 prints a hash

- command: `git -C <clone> rev-parse --verify -q '8d781db20c882f9b1a4bf62608729a0ce580b524^2'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (merge-sha = 8d781db20c882f9b1a4bf62608729a0ce580b524)
- output:

```text
cc75204a583001a568dbfc1497bc2f61c7c95582
```

## 4. Step 3: <merge-sha>^3 prints nothing and exits 1

- command: `git -C <clone> rev-parse --verify -q '8d781db20c882f9b1a4bf62608729a0ce580b524^3'`
- exit code: 1
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 5. Step 3: ^1 equals the recorded master tip and ^2 equals the recorded reviewed head

- command: `git -C <clone> rev-parse '8d781db20c882f9b1a4bf62608729a0ce580b524^1' '8d781db20c882f9b1a4bf62608729a0ce580b524^2'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (recorded master tip 9e78b108761ccecb3883ab9a21415bc7afa7cecd; recorded head cc75204a583001a568dbfc1497bc2f61c7c95582)
- output:

```text
9e78b108761ccecb3883ab9a21415bc7afa7cecd
cc75204a583001a568dbfc1497bc2f61c7c95582
```

## 6. Step 3: the merge tree equals the reviewed head tree

- command: `git -C <clone> rev-parse '8d781db20c882f9b1a4bf62608729a0ce580b524^{tree}' 'cc75204a583001a568dbfc1497bc2f61c7c95582^{tree}'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
ca342ad67bb689b6c83b6ea669cdebec1a094a41
ca342ad67bb689b6c83b6ea669cdebec1a094a41
```

## 7. Step 3: a squash-shaped commit has no ^2 (the capture block stops before tagging)

- command: `git -C <clone> rev-parse --verify -q 'dd92ac89be85d6aab574da33eb56ebc9ceeddb65^2'`
- exit code: 1
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (squash commit dd92ac89be85d6aab574da33eb56ebc9ceeddb65)
- output:

```text

```

## 8. Step 3: when master moves after Step 2, ^1 no longer equals the recorded master tip (the check fails, so the run stops)

- command: `git -C <clone> rev-parse 'c483a89dd8d3fd9642767b566b9abfdfd1759505^1'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (extra commit 74f5fa639aca4b192db6122610f7e4fbdab1f9ad; merge c483a89dd8d3fd9642767b566b9abfdfd1759505)
- output:

```text
74f5fa639aca4b192db6122610f7e4fbdab1f9ad
```

## 9. Step 3: when master moves after Step 2, the trees differ (second failing check)

- command: `git -C <clone> rev-parse 'c483a89dd8d3fd9642767b566b9abfdfd1759505^{tree}' 'cc75204a583001a568dbfc1497bc2f61c7c95582^{tree}'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
3e23faad1ca8cdf562d38626c802b2d712bf1faf
ca342ad67bb689b6c83b6ea669cdebec1a094a41
```

## 10. Step 4: the tag does not exist locally before tagging (prints nothing)

- command: `git -C <clone> tag --list rehearsal-0.0.0`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 11. Step 4: the tag does not exist on origin before tagging (prints nothing)

- command: `git -C <clone> ls-remote --tags origin rehearsal-0.0.0`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 12. Step 4: tag the merge commit and push the tag (the && form of the page)

- command: `git -C <clone> tag -a rehearsal-0.0.0 <merge-sha> -m ... && git -C <clone> push origin rehearsal-0.0.0`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (remote get-url origin printed the temporary bare repository before the push)
- output:

```text
To /tmp/rehearsal-826-joeqqaw_/origin.git
 * [new tag]         rehearsal-0.0.0 -> rehearsal-0.0.0
```

## 13. Step 4: ls-remote with ^{} prints the merge SHA (the commit the annotated tag points to)

- command: `git -C <clone> ls-remote origin 'refs/tags/rehearsal-0.0.0^{}'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
8d781db20c882f9b1a4bf62608729a0ce580b524	refs/tags/rehearsal-0.0.0^{}
```

## 14. Step 4: rev-parse <tag>^{commit} prints the merge SHA

- command: `git -C <clone> rev-parse 'rehearsal-0.0.0^{commit}'`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
8d781db20c882f9b1a4bf62608729a0ce580b524
```

## 15. Step 4: ls-remote --tags without ^{} prints the tag object, not the merge SHA

- command: `git -C <clone> ls-remote --tags origin rehearsal-0.0.0`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (tag object 7a18bd325069e2a46718effe27d53b8f9ec9e4e7)
- output:

```text
7a18bd325069e2a46718effe27d53b8f9ec9e4e7	refs/tags/rehearsal-0.0.0
```

## 16. Step 4: the tag is annotated (git cat-file -t prints tag)

- command: `git -C <clone> cat-file -t rehearsal-0.0.0`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
tag
```

## 17. Step 5: the proof is 1 before the merge-back

- command: `git -C <clone> merge-base --is-ancestor 8d781db20c882f9b1a4bf62608729a0ce580b524 origin/integration`
- exit code: 1
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 18. Step 5: the merge-back changes 0 files (diff of the merge-back against its first parent prints nothing)

- command: `git -C <clone> diff --name-only '27861bb693b25e853b1636ee1fbaa63bc24bc277^1' 27861bb693b25e853b1636ee1fbaa63bc24bc277`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (merge-back commit 27861bb693b25e853b1636ee1fbaa63bc24bc277)
- output:

```text

```

## 19. Step 5: the proof is 0 after the merge-back

- command: `git -C <clone> merge-base --is-ancestor 8d781db20c882f9b1a4bf62608729a0ce580b524 origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 20. Step 5: the Step 2 precondition of the next release is 0 after the merge-back

- command: `git -C <clone> merge-base --is-ancestor origin/master origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 21. Step 5: the proof is still 0 after a newer commit lands on integration

- command: `git -C <clone> merge-base --is-ancestor 8d781db20c882f9b1a4bf62608729a0ce580b524 origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (newer commit 9ba0ac34f05a90cba1516acf34f345a16ebc7f4e)
- output:

```text

```

## 22. Step 5: a second run of the first is-ancestor line exits 0, so the page says: record already merged back and skip the last two lines

- command: `git -C <clone> merge-base --is-ancestor 8d781db20c882f9b1a4bf62608729a0ce580b524 origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (result recorded: already merged back)
- output:

```text

```

## 23. Skill Wave 1: git ls-remote --symref origin HEAD prints ref: refs/heads/integration

- command: `git -C <clone> ls-remote --symref origin HEAD`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
ref: refs/heads/integration	HEAD
9ba0ac34f05a90cba1516acf34f345a16ebc7f4e	HEAD
```

## 24. Skill Wave 1: git fetch origin <default-branch> --tags succeeds

- command: `git -C <clone> fetch origin integration --tags`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text
From /tmp/rehearsal-826-joeqqaw_/origin
 * branch            integration -> FETCH_HEAD
```

## 25. Skill Wave 1: with a stale local integration, the bare local branch name gives exit 1

- command: `git -C <clone> merge-base --is-ancestor rehearsal-0.0.0 integration`
- exit code: 1
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (local integration reset to cc75204a583001a568dbfc1497bc2f61c7c95582)
- output:

```text

```

## 26. Skill Wave 1: refs/remotes/origin/<default-branch> after a fetch gives exit 0

- command: `git -C <clone> merge-base --is-ancestor rehearsal-0.0.0 refs/remotes/origin/integration`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed**
- output:

```text

```

## 27. Skill Wave 1: with refs/remotes/origin/HEAD set to master the offline fallback resolves master (stale: it disagrees with the live value integration)

- command: `git -C <clone> symbolic-ref refs/remotes/origin/HEAD`
- exit code: 0
- `git rev-parse --show-toplevel`: `/tmp/rehearsal-826-joeqqaw_/clone` (equals the temporary clone)
- result: **passed** (the skill text says a value from this fallback is reported as unverified)
- output:

```text
refs/remotes/origin/master
```

## 28. Skill Wave 1: the skill text reports a fallback value as unverified

- command: `read of src/superclaude/skills/sc-post-release-protocol/SKILL.md (read-only, real repository)`
- exit code: 0
- `git rev-parse --show-toplevel`: `(not a clone command)` (equals the temporary clone)
- result: **passed** (text check, no git run in the clone)
- output:

```text
the paragraph says: only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`; if ... the value came from the fallback, report the ancestry check as **unverified**
```

## Not exercised here (GitHub-only)

- `gh pr merge --match-head-commit`: not exercised
- `gh pr view fields (state, baseRefName, headRefName, headRefOid, mergeCommit)`: not exercised
- `gh run list --commit`: not exercised
- `gh release create --verify-tag`: not exercised
- `gh pr checks --watch with no checks`: not exercised

## State of the real repository

- status lines outside this package's folder identical: True (before 188 lines, after 189 lines; lines inside `.dev/tasks/to-do/TASK-WF-designR1-20261126-070747` are ignored)
- `git rev-parse HEAD` identical: True
- `git symbolic-ref -q refs/remotes/origin/HEAD` identical: True
- `git tag --list 'rehearsal-*'` identical: True

Before: `./artifacts/t12-state-before.txt`; after: `./artifacts/t12-state-after.txt`.
