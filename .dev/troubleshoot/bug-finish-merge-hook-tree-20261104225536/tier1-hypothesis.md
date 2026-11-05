# Hypothesis: finish-merge.sh never ties the published merge commit to the index its gate validated

**Agent**: root-cause-analyst (lens; worker troubleshoot-analyst)
**Tier**: 1
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing post-condition (hooks run between checking the index and making the commit); the design follows it (doc-context.md)
**Claim class**: `runtime_behavior`
**Evidence class**: `runtime_repro` (parent probe, tier1-observation.md ## Probe)
**Verdict direction**: `AFFIRM` (confirms C4)
**Consistency with docs**: aligned (matches design 7.2 and the refs as written; the docs share the gap, so the fix extends them without contradicting them)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh commit mode steps 5-8 @ local operator checkout (bash, git, repository commit hooks)

producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
Steps 2-5 prove properties of the index. Step 6 runs `git commit` with hooks on, and git commits the index as the hook leaves it (behaviour-definition: row 1). Step 7 checks only the parents; step 8 only that the work tree and index match the new commit. A pre-commit hook that edits and stages a file therefore changes the published tree, the work tree stays clean against it, and the script exits 0. The cause is the missing comparison between the validated tree and `HEAD^{tree}`.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | tier1-observation.md `## Probe` (probe-c4.out:1-5) | exit 0 with a merge_sha; validated tree 75418c01... vs committed tree 1eea654f...; HEAD:unrelated.txt = "changed by hook" |
| E2 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:262-269 | step 5, the last check before the commit |
| E3 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:271-276 | step 6 `git commit -F "$MESSAGE_FILE"` with hooks on; no tree recorded beforehand (at 62121669) |
| E4 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:288-292 | step 8 checks only status and `diff --quiet HEAD` (at 62121669) |
| E5 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:124 | `tree_dirty` after the commit -> merge_preflight_dirty, commit named, nothing pushed |
| E6 | test_assertion | tests/pr_submit/test_conflict_scripts.py:960-979 | only a rejecting hook (F9) covered |

## Proposed Fix
1. After step 5 and before step 6: `VALIDATED_TREE="$(git write-tree 2>"$TMP/err")" || { ...; fail tree_dirty "cannot record ..."; }` (a tree object; no ref or index change).
2. Step 8, before the status check: `COMMIT_TREE="$(git rev-parse -q --verify 'HEAD^{tree}')"`; if it differs from VALIDATED_TREE, `fail tree_dirty` naming the new commit and saying a commit hook changed staged content; nothing pushed. Exactly one `git commit` match remains; no banned word; no new token; HALT_REASONS and SKILL.md:331 unchanged.
3. Header (:9-10) notes the tree object; step 8 comment updated.
4. refs/conflict-mechanical.md :114 (the post-commit tree check), :124 (row text), :294 (the hook-changed-commit message).
5. Tests: P-1 hook rewrites and stages an unrelated file -> FINISH_FAIL tree_dirty, new sha in stderr; P-2 hook changes nothing -> exit 0.

## Confidence
Self-reported 0.93 (calibrator re-grades).

## Risks
- A failed write-tree maps to tree_dirty before the commit (message wording approximate; rare, step 2 guarantees no unmerged entries).
- Hooks that legitimately reformat files now halt the run (intended: validation must cover what is published).

## If I'm wrong, it's probably because...
The C4 effect came from a post-commit hook rewriting HEAD; the probe installed only a pre-commit hook and the committed tree differs, which excludes it.

## Falsification standard
True: P-1 exits 0 with a merge_sha before the fix (observed, probe-c4.out:2) and `FINISH_FAIL tree_dirty`, exit 2, new sha in stderr after it; P-2 exits 0 after the fix. False: P-1 still exits 0 after the fix, or P-2 yields tree_dirty (the recorded tree is wrong).

## Alternatives considered
- --no-verify, amend or reset: banned (J-60, conflict-mechanical.md:277, the static-rule test).
- Running the hook before validation (`git hook run`): the commit runs it again; needs git 2.36+.
- Re-running steps 4-5 against HEAD^{tree}: works but larger; tree-id comparison is exact.
