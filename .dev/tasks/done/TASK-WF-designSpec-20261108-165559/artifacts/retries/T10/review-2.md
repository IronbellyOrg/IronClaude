# Review 2: T10 spec compliance

Reviewed tree: refs/superclaude/implement/TASK-WF-designSpec-20261108-165559/retry/T10/r1-2 (tree bbd80ccfe3ba99407887797185865d31ca62b02c, equal to the live worktree), start sha 1846880a8e48911994a61b896dd13be862501a2a.

## Earlier blocking findings

F1.1 resolved: every edited doc now says the IR-7 refusal path "arrives switched off in the separate last #441 commit" instead of stating it is already built (docs/designs/sc-issue-launch-level-hook.md:34, :355, :516, :615; docs/designs/sc-issue-claim-pipeline-flag.md:4, :60; src/superclaude/skills/sc-issue-protocol/SKILL.md:92; src/superclaude/commands/issue.md:16; docs/user-guide/commands.md:381). This matches the live code note at src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1684 ("the off IR7_REFUSE switch comes in a later commit") and OD-3.
F1.2 resolved: the forward reference to `artifacts/final-check-retest.md` is removed; docs/designs/sc-issue-launch-level-hook.md:559 now says only that the `final-check.md` limits are not edited.
F1.3 resolved: docs/designs/sc-issue-launch-level-hook.md:617 now says "the selector returns `ordinary`, so the stream is not read", which matches the hook: an ordinary actor exits before `l2_read` (src/superclaude/hooks/scripts/launch-level-pre-push.sh:188-189).
F1.4 resolved: §19.2 now defines `stale` as "when it carries a `# launch-level-pre-push-version:` line but differs from the installed copy" (docs/designs/sc-issue-launch-level-hook.md:514), which matches the code (orca_worktree.py:1226, `_L2_VERSION_PREFIX.encode() in body`) and LIM-17 (:554).

## Acceptance criteria

- T10.AC1 met: no edited doc says an absent L2 refuses the launch; each says `W-L2-ABSENT` is a warning while `IR7_REFUSE` is `False`. Citations: T10.AC1@docs/designs/sc-issue-launch-level-hook.md:516, T10.AC1@docs/designs/sc-issue-launch-level-hook.md:355, T10.AC1@docs/designs/sc-issue-claim-pipeline-flag.md:4, T10.AC1@docs/designs/sc-issue-claim-pipeline-flag.md:291, T10.AC1@src/superclaude/skills/sc-issue-protocol/SKILL.md:92, T10.AC1@src/superclaude/commands/issue.md:16, T10.AC1@docs/user-guide/commands.md:381. The "refuse ... when ... L2 is missing" text at docs/designs/sc-issue-claim-pipeline-flag.md:60 is the source-requirement column; its "Built" column on the same row says a missing L2 gives the warning.
- T10.AC2 met: §19.8 holds the measured cost table (no hook 19 ms, hook 120 ms / 115 ms median) and the method (host, git and uv versions, 15 pushes per case, `date +%s%N`, temporary HOME, selector result). Citation: T10.AC2@docs/designs/sc-issue-launch-level-hook.md:617. No test changed between the start sha and this tree (`git diff --stat 1846880a8 -- tests` is empty); the only timing calls in tests/hooks/test_launch_level_pre_push.py:66-67 are a wait loop, not a latency bound.
- T10.AC3 met: `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` gives 168 text lines, the same as `git grep` at the start sha (168); both edited primitives have 0 hits before and after (src/superclaude/commands/issue.md:16, src/superclaude/skills/sc-issue-protocol/SKILL.md:92). `make verify-sync` printed "All components in sync." with exit 0. No `plugins/superclaude/` mirror exists for either edited primitive. Citation: T10.AC3@src/superclaude/skills/sc-issue-protocol/SKILL.md:92.

## Findings

None.

Self-Audit: re-read the delta diff and the live lines it touched (§19.2 :514-516, LIM table and :559, §19.8 :608-627); grepped all five edited docs for `IR7_REFUSE`, "refusal path", "is built" and absent-L2 phrasings; checked orca_worktree.py for `IR7_REFUSE` (only the two "later commit" comments at :53 and :1684) and the `stale` rule at :1226; checked the pre-push hook's ordinary exit at :188; compared the NFR-003 grep count with the start sha; ran `make verify-sync`; confirmed no test diff. Non-blocking note: the frontmatter status line (docs/designs/sc-issue-launch-level-hook.md:6) lists the refusal path under "built:" as "added switched off by the separate last #441 commit"; it names the later commit, so it is accurate once commit E lands, and that matches OD-3.
