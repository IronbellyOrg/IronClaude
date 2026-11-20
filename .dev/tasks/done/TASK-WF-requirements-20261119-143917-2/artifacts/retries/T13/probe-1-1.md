037a20427733cd81a9a0cc2989110c4500579e1c
family design-doc-h3-stale: a design document line still describes the issue verbs as SUBMIT
command: git grep -n -e "issue create|edit|comment" -e "issue create, edit" -- docs src tests
before: docs/designs/sc-issue-launch-level-hook.md:172 named the three issue verbs under SUBMIT
coupled sites: the same file's grid rows (lines 95 to 110) and message table (LL-SUBMIT, LL-ISSUE)
after: line 172 names group issue, label or project as ISSUE and the two project reads as NONE
