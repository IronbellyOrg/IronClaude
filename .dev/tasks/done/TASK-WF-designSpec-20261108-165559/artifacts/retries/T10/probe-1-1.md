1846880a8e48911994a61b896dd13be862501a2a
# Family probe, T10 review 1 (blocking families F1.1-F1.4)

Files searched (F): docs/designs/sc-issue-launch-level-hook.md docs/designs/sc-issue-claim-pipeline-flag.md src/superclaude/skills/sc-issue-protocol/SKILL.md src/superclaude/commands/issue.md docs/user-guide/commands.md

## F1.1 forward-dated-ir7-claim
Defect form: a doc states as present fact that the IR-7 refusal path "is built" / "#441 built ... the IR-7 refusal path", while the code arrives only in commit E (the separate last #441 commit).
Command: grep -n -F -e 'built but' -e 'IR-7 refusal path, but' -e 'and the IR-7 refusal path' -e 'is built.' -e 'is built and' -- F
before:
- docs/designs/sc-issue-launch-level-hook.md:6 "its refusal path built but switched off"
- docs/designs/sc-issue-launch-level-hook.md:34 "its refusal path is built but switched off"
- docs/designs/sc-issue-launch-level-hook.md:202 "no `cwd` fallback is built." (inherited, unrelated: not this family)
- docs/designs/sc-issue-launch-level-hook.md:355 "The refusal path is built but switched off"
- docs/designs/sc-issue-launch-level-hook.md:516 "The refusal path (no launch record, no agent) is built and switches on"
- docs/designs/sc-issue-launch-level-hook.md:615 "The IR-7 refusal path is built but switched off"
- docs/designs/sc-issue-claim-pipeline-flag.md:4 "#441 built the L2 layer and its IR-7 refusal path"
- docs/designs/sc-issue-claim-pipeline-flag.md:60 "#441 built the L2 layer and the IR-7 refusal path"
- src/superclaude/skills/sc-issue-protocol/SKILL.md:92 "the IR-7 refusal is built but switched off"
- src/superclaude/commands/issue.md:16 "the IR-7 refusal is built but switched off"
- docs/user-guide/commands.md:381 "the IR-7 refusal is built but switched off"
Coupled sites: claim-flag :135 and :291 ("while `IR7_REFUSE` is `False` (#441)") are conditional, no existence claim; left as is.
after: docs/designs/sc-issue-launch-level-hook.md:202 only (inherited, unrelated). All ten family sites now say the refusal path "arrives switched off in the separate last #441 commit" (true at commit D and commit E). Extra check `grep -i -E 'refusal (path )?(is )?built|built (the|its) IR-7'` over F: no hits.

## F1.2 forward-dated-reference
Defect form: a doc points at a package artifact that does not exist yet.
Command: grep -n -F -e 'final-check-retest' -- F
before: docs/designs/sc-issue-launch-level-hook.md:559
Coupled sites: none. Task 11 creates the file and re-adds the pointer.
after: no hits (pointer removed from :559; Task 11 re-adds it with the file).

## F1.3 measurement-method-text
Defect form: the §19.8 method text names the wrong selector result.
Command: grep -n -F -e 'returns `unknown`' -- F
before: docs/designs/sc-issue-launch-level-hook.md:617
Coupled sites: none.
after: no hits (:617 now says the selector returns `ordinary`, so the stream is not read).

## F1.4 stale-reason-definition
Defect form: `stale` defined as "an older version line"; code (orca_worktree.py:1226) and LIM-17 (:554) mean any differing body with the version prefix.
Command: grep -n -F -e 'older version line' -- F
before: docs/designs/sc-issue-launch-level-hook.md:514
Coupled sites: LIM-17 at :554 (already correct).
after: no hits (:514 now matches LIM-17: a version line but differs from the installed copy).
