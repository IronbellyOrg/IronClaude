# .gitignore check (item 8.6)

Run 2026-11-12T01:47:19Z in the worktree.

## Check 1: `.dev/sweeps/` is ignored

Command: `git check-ignore -q .dev/sweeps/x.md; echo $?`

~~~
0
~~~

PASS: 0 (expected 0).

## Check 2: `.dev/tasks/` is not ignored

Command: `git check-ignore -q .dev/tasks/to-do/x.md; echo $?`

~~~
1
~~~

PASS: 1 (expected 1).

## Check 3: two insertions in `.gitignore`

Command: `git diff --stat -- .gitignore`

~~~
 .gitignore | 2 ++
 1 file changed, 2 insertions(+)
~~~

PASS: 2 insertions, 0 deletions (expected 2 insertions).

## Result

3 PASS lines, 0 FAIL lines.

.gitignore check: PASS
